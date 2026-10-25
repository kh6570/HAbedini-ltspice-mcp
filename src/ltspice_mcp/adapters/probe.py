# In the name of God, the Most Gracious, the Most Merciful
"""This module probes the capability of the LTspice executable.

Version detection uses the Windows PE file-version resource. LTspice has no
documented ``--version`` switch. The probe does not launch the GUI during startup.
"""

from __future__ import annotations

import ctypes
import os
import sys
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from typing import TYPE_CHECKING, Literal

ProbeSource = Literal["configured", "default-location", "path", "unavailable"]
VersionSource = Literal["metadata", "unavailable"]

if TYPE_CHECKING:
    from ltspice_mcp.infra.config import LTspiceSettings


@dataclass(frozen=True, slots=True)
class ProbeResult:
    """Summary of the discovered LTspice executable and its sibling bridge."""

    configured: bool
    executable: Path | None
    exists: bool
    source: ProbeSource
    version: str | None = None
    version_source: VersionSource = "unavailable"
    note: str = ""
    bridge_executable: Path | None = None
    bridge_exists: bool = False
    message_bridge: bool = False

    def summary(self) -> dict[str, object]:
        """Return a JSON-serializable probe summary."""

        return {
            "configured": self.configured,
            "executable": str(self.executable) if self.executable is not None else None,
            "exists": self.exists,
            "source": self.source,
            "version": self.version,
            "version_source": self.version_source,
            "note": self.note,
            "bridge_executable": (
                str(self.bridge_executable) if self.bridge_executable is not None else None
            ),
            "bridge_exists": self.bridge_exists,
            "message_bridge": self.message_bridge,
        }


def default_install_locations() -> tuple[Path, ...]:
    """Return the default Windows install locations that the probe checks."""

    program_files = Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
    local_app = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
    return (
        program_files / "LTC" / "LTspiceXVII" / "XVIIx64.exe",
        program_files / "ADI" / "LTspice" / "LTspice.exe",
        local_app / "Programs" / "ADI" / "LTspice" / "LTspice.exe",
        program_files / "LTC" / "LTspiceXVII" / "XVIIx86.exe",
    )


def discover_executable(configured_executable: Path | None) -> tuple[Path | None, ProbeSource]:
    """Return the configured executable or the first discovered fallback."""

    if configured_executable is not None:
        return configured_executable.resolve(strict=False), "configured"
    for candidate in default_install_locations():
        if candidate.is_file():
            return candidate.resolve(strict=False), "default-location"
    for candidate_name in ("XVIIx64.exe", "LTspice.exe", "XVIIx86.exe"):
        discovered_path = which(candidate_name)
        if discovered_path is not None:
            return Path(discovered_path).resolve(strict=False), "path"
    return None, "unavailable"


def _detect_version_metadata(executable: Path) -> tuple[str | None, VersionSource]:
    """Read the PE file version resource on Windows."""

    if sys.platform != "win32":
        return None, "unavailable"

    class VsFixedFileInfo(ctypes.Structure):
        _fields_ = (
            ("signature", wintypes.DWORD),
            ("struc_version", wintypes.DWORD),
            ("file_version_ms", wintypes.DWORD),
            ("file_version_ls", wintypes.DWORD),
            ("product_version_ms", wintypes.DWORD),
            ("product_version_ls", wintypes.DWORD),
            ("file_flags_mask", wintypes.DWORD),
            ("file_flags", wintypes.DWORD),
            ("file_os", wintypes.DWORD),
            ("file_type", wintypes.DWORD),
            ("file_subtype", wintypes.DWORD),
            ("file_date_ms", wintypes.DWORD),
            ("file_date_ls", wintypes.DWORD),
        )

    try:
        version_dll = ctypes.WinDLL("version", use_last_error=True)
        size = version_dll.GetFileVersionInfoSizeW(str(executable), None)
        if not size:
            return None, "unavailable"
        buffer = ctypes.create_string_buffer(size)
        if not version_dll.GetFileVersionInfoW(str(executable), 0, size, buffer):
            return None, "unavailable"
        info_ptr = ctypes.c_void_p()
        info_len = wintypes.UINT()
        queried = version_dll.VerQueryValueW(
            buffer,
            "\\",
            ctypes.byref(info_ptr),
            ctypes.byref(info_len),
        )
        if not queried or not info_ptr:
            return None, "unavailable"
        info = ctypes.cast(info_ptr, ctypes.POINTER(VsFixedFileInfo)).contents
        file_ms = int(info.file_version_ms)
        file_ls = int(info.file_version_ls)
        version = f"{file_ms >> 16}.{file_ms & 0xFFFF}.{file_ls >> 16}.{file_ls & 0xFFFF}"
    except (OSError, AttributeError, ctypes.ArgumentError):
        return None, "unavailable"
    return version, "metadata"


def schematic_version_line(exe_version: str | None) -> str:
    """Return the ``Version`` header to write for this LTspice generation.

    LTspice XVII reads and writes ``Version 4``. LTspice 24 writes ``Version 4.1``.
    A read accepts both.
    """

    if exe_version is None:
        return "Version 4"
    major_text = exe_version.split(".", maxsplit=1)[0]
    if major_text.isdigit() and int(major_text) >= 24:
        return "Version 4.1"
    return "Version 4"


def version_at_least(version: str | None, major: int, minor: int) -> bool:
    """Return True when ``version`` is at least ``major.minor``."""

    if version is None:
        return False
    numbers: list[int] = []
    for piece in version.split("."):
        if not piece.isdigit():
            return False
        numbers.append(int(piece))
    if len(numbers) < 2:
        return False
    return (numbers[0], numbers[1]) >= (major, minor)


def bridge_executable_for(executable: Path | None) -> Path | None:
    """Return a sibling ``ltspice-mcp-bridge.exe`` when that file exists."""

    if executable is None:
        return None
    candidate = executable.resolve(strict=False).parent / "ltspice-mcp-bridge.exe"
    if candidate.is_file():
        return candidate
    return None


def library_root(executable: Path | None) -> Path | None:
    """Return the LTspice ``lib`` directory next to the executable, if present."""

    if executable is None:
        return None
    candidate = executable.resolve(strict=False).parent / "lib"
    if candidate.is_dir():
        return candidate
    return None


def probe_ltspice(settings: LTspiceSettings) -> ProbeResult:
    """Discover the LTspice executable that the settings describe."""

    executable, source = discover_executable(settings.exe)
    if executable is None:
        return ProbeResult(
            configured=settings.exe is not None,
            executable=None,
            exists=False,
            source="unavailable",
            note="LTspice was not found. Set LTSPICE_EXE or install LTspice.",
        )
    exists = executable.is_file()
    version: str | None = None
    version_source: VersionSource = "unavailable"
    if exists:
        version, version_source = _detect_version_metadata(executable)
    note = "LTspice executable is available." if exists else "Configured executable is missing."
    bridge = bridge_executable_for(executable) if exists else None
    bridge_ready = bridge is not None and version_at_least(version, 26, 1)
    if bridge_ready:
        note = "LTspice 26.1 or newer is available and ltspice-mcp-bridge.exe is beside it."
    return ProbeResult(
        configured=settings.exe is not None,
        executable=executable,
        exists=exists,
        source=source,
        version=version,
        version_source=version_source,
        note=note,
        bridge_executable=bridge,
        bridge_exists=bridge is not None,
        message_bridge=bridge_ready,
    )


def build_summary(settings: LTspiceSettings) -> dict[str, object]:
    """Return the probe summary that ``--setup`` uses."""

    return probe_ltspice(settings).summary()
