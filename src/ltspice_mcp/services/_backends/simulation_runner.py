# In the name of God, the Most Gracious, the Most Merciful
"""Launch LTspice batch and netlist commands."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from ltspice_mcp.adapters.cli.ltspice_v1 import (
    build_batch_command,
    build_netlist_command,
    classify_simulation_log,
)
from ltspice_mcp.adapters.probe import probe_ltspice
from ltspice_mcp.core.exceptions import (
    ArtifactMissingError,
    BackendUnavailableError,
    SimulationError,
)
from ltspice_mcp.infra.subprocess_runner import run_command
from ltspice_mcp.services._backends.text_decode import read_ltspice_text
from ltspice_mcp.services._internals.active_runs import pop_run, register_run

if TYPE_CHECKING:
    import subprocess

    from ltspice_mcp.adapters.base import SimulationCommand
    from ltspice_mcp.infra.config import LTspiceSettings

def resolve_executable(settings: LTspiceSettings, explicit: Path | None) -> Path:
    """Return a probed LTspice executable or raise."""

    if explicit is not None and explicit.is_file():
        return explicit
    probed = probe_ltspice(settings)
    if probed.executable is None or not probed.exists:
        raise BackendUnavailableError(probed.note or "LTspice is not installed.")
    return probed.executable


def _cache_dir(settings: LTspiceSettings) -> Path:
    root = (settings.cache_dir or Path.cwd() / ".ltspice-mcp-cache") / "simulation"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _fingerprint(
    source: Path,
    *,
    executable: Path,
    ascii_raw: bool,
    extra_switches: tuple[str, ...],
) -> str:
    digest = hashlib.sha256()
    digest.update(source.read_bytes())
    digest.update(str(executable).encode("utf-8"))
    digest.update(b"\0ascii" if ascii_raw else b"\0binary")
    digest.update("\0".join(extra_switches).encode("utf-8"))
    return digest.hexdigest()


def _restore_cached(bucket: Path, command_paths: tuple[Path, ...]) -> bool:
    if not (bucket / "ok").is_file():
        return False
    for path in command_paths:
        cached = bucket / path.name
        if cached.is_file():
            shutil.copyfile(cached, path)
    return True


def _store_cache(bucket: Path, paths: tuple[Path, ...]) -> None:
    bucket.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if path.is_file():
            shutil.copyfile(path, bucket / path.name)
    (bucket / "ok").write_text("ok", encoding="utf-8")


def run_netlist(
    source: Path,
    *,
    settings: LTspiceSettings,
    executable: Path | None,
) -> Path:
    """Ask LTspice to write the sibling ``.net`` file."""

    exe = resolve_executable(settings, executable)
    command = build_netlist_command(exe, source)
    result = run_command(
        list(command.argv),
        cwd=command.cwd,
        timeout_s=settings.resolve_timeout_s(None),
    )
    netlist = command.netlist_path
    if netlist is None or not netlist.is_file():
        detail = result.stderr.strip() or result.stdout.strip() or "no netlist was written"
        raise SimulationError(detail, exit_code=result.return_code, stderr=result.stderr)
    return netlist


def run_simulation(
    source: Path,
    *,
    settings: LTspiceSettings,
    executable: Path | None,
    ascii_raw: bool = True,
    timeout_s: float | None = None,
    extra_switches: tuple[str, ...] = (),
    use_cache: bool = True,
) -> dict[str, object]:
    """Run one batch simulation and return the artifact paths."""

    exe = resolve_executable(settings, executable)
    batch_source = source
    if source.suffix.lower() == ".asc":
        batch_source = run_netlist(source, settings=settings, executable=exe)
    command = build_batch_command(
        exe,
        batch_source,
        ascii_raw=ascii_raw,
        extra_switches=extra_switches,
    )
    outputs = tuple(
        path for path in (command.log_path, command.raw_path, command.netlist_path) if path
    )
    bucket = _cache_dir(settings) / _fingerprint(
        source, executable=exe, ascii_raw=ascii_raw, extra_switches=extra_switches
    )
    if use_cache and _restore_cached(bucket, outputs):
        log_text = read_ltspice_text(command.log_path) if command.log_path.is_file() else ""
        return _result_payload(command, log_text, cache_hit=True, return_code=0)

    def _on_start(process: subprocess.Popen[str]) -> None:
        register_run(str(source.resolve()), process)

    try:
        completed = run_command(
            list(command.argv),
            cwd=command.cwd,
            timeout_s=settings.resolve_timeout_s(timeout_s),
            on_start=_on_start,
        )
    finally:
        pop_run(str(source.resolve()))

    if not command.log_path.is_file():
        raise ArtifactMissingError(f"LTspice did not write a log at {command.log_path}.")
    log_text = read_ltspice_text(command.log_path)
    classify_simulation_log(log_text, return_code=completed.return_code)
    if command.raw_path is not None and not command.raw_path.is_file():
        raise ArtifactMissingError(f"LTspice did not write a raw file at {command.raw_path}.")
    if use_cache:
        _store_cache(bucket, outputs)
    return _result_payload(command, log_text, cache_hit=False, return_code=completed.return_code)


def _result_payload(
    command: SimulationCommand,
    log_text: str,
    *,
    cache_hit: bool,
    return_code: int,
) -> dict[str, object]:
    return {
        "cache_hit": cache_hit,
        "return_code": return_code,
        "command": list(command.argv),
        "log_path": str(command.log_path),
        "raw_path": str(command.raw_path) if command.raw_path is not None else None,
        "netlist_path": str(command.netlist_path) if command.netlist_path is not None else None,
        "log_excerpt": "\n".join(log_text.splitlines()[-20:]),
    }
