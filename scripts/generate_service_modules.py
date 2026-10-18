# In the name of God, the Most Gracious, the Most Merciful
"""Write one module and one contract row per service function.

Run from the repository root after the operations modules exist.
"""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

PACKAGES = (
    "schematic",
    "subcircuit",
    "simulation",
    "batch",
    "remote",
    "waveform",
    "artifacts",
    "symbols",
    "live_gui",
    "workspace",
    "instructions",
    "recipes",
    "topology",
)
SKIP = {"clean_netlist_text", "directive_commands", "count_records", "raw_flags"}
SKIP_PARAMS = {"workspace_root", "settings", "ltspice_executable", "use_simulator"}
LONG_RUNNING = {
    "run_simulation",
    "run_value_sweep",
    "run_param_sweep",
    "run_model_sweep",
    "run_monte_carlo",
    "run_worst_case",
    "submit_batch",
    "submit_remote_simulation",
}
READ_PREFIXES = (
    "list_",
    "read_",
    "describe_",
    "inspect_",
    "check_",
    "compare_",
    "measure_",
    "compute_",
    "suggest_",
    "resolve_",
    "summarize_",
    "get_",
    "poll_",
    "search_",
    "validate_",
)


def _tool_name(func_name: str) -> str:
    if func_name.endswith("_service"):
        return func_name[: -len("_service")]
    return func_name


def _title(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("_"))


def _summary(fn: Any) -> str:
    doc = inspect.getdoc(fn) or _title(_tool_name(fn.__name__))
    return doc.splitlines()[0].strip()


def _schema_type(annotation: Any) -> dict[str, object]:
    text = getattr(annotation, "__name__", str(annotation))
    rendered = str(annotation)
    if annotation is int or ("int" in rendered and "float" not in rendered):
        return {"type": "integer"}
    if annotation is float or rendered.startswith("float"):
        return {"type": "number"}
    if annotation is bool or rendered.startswith("bool"):
        return {"type": "boolean"}
    if "tuple" in rendered or "list" in rendered:
        return {"type": "array", "items": {"type": "string"}}
    if text in {"int"}:
        return {"type": "integer"}
    return {"type": "string"}


def _schema(fn: Any) -> dict[str, object]:
    hints = {}
    try:
        hints = inspect.get_annotations(fn, eval_str=True)
    except Exception:
        hints = getattr(fn, "__annotations__", {})
    properties: dict[str, object] = {}
    required: list[str] = []
    for name, parameter in inspect.signature(fn).parameters.items():
        if name in SKIP_PARAMS:
            continue
        annotation = hints.get(name, str)
        properties[name] = _schema_type(annotation)
        if parameter.default is inspect.Parameter.empty:
            required.append(name)
    return {"type": "object", "properties": properties, "required": required}


def _module_text(package: str, tool: str, func_name: str, summary: str, spec: str) -> str:
    import_line = (
        f"from ltspice_mcp.services.{package}.operations import {func_name} as {tool}"
        if func_name != tool
        else f"from ltspice_mcp.services.{package}.operations import {tool}"
    )
    return (
        f'"""{summary}"""\n\n'
        "from __future__ import annotations\n\n"
        f"{import_line}\n"
        "from ltspice_mcp.services.service_spec import ServiceSpec\n\n"
        f"{spec}\n"
    )


def main() -> None:
    for package in PACKAGES:
        module = __import__(
            f"ltspice_mcp.services.{package}.operations",
            fromlist=["operations"],
        )
        contracts: dict[str, dict[str, object]] = {}
        package_dir = SRC / "ltspice_mcp" / "services" / package
        for func_name, fn in inspect.getmembers(module, inspect.isfunction):
            if fn.__module__ != module.__name__ or func_name.startswith("_") or func_name in SKIP:
                continue
            tool = _tool_name(func_name)
            summary = _summary(fn)
            read_only = tool.startswith(READ_PREFIXES)
            destructive = tool.startswith(("remove_", "cancel_"))
            spec = (
                "SERVICE_SPEC = ServiceSpec(\n"
                f"    name={tool!r},\n"
                f"    title={_title(tool)!r},\n"
                f"    summary={summary!r},\n"
                '    phase="implemented",\n'
                f"    read_only={read_only},\n"
                f"    long_running={tool in LONG_RUNNING},\n"
                f"    destructive={destructive},\n"
                f"    idempotent={read_only},\n"
                ")\n"
            )
            (package_dir / f"{tool}.py").write_text(
                _module_text(package, tool, func_name, summary, spec),
                encoding="utf-8",
            )
            contracts[tool] = {
                "title": _title(tool),
                "description": summary,
                "input_schema": _schema(fn),
            }
        body = (
            '"""Generated MCP contracts."""\n\n'
            "from __future__ import annotations\n\n"
            f"MCP_CONTRACTS: dict[str, dict[str, object]] = {json.dumps(contracts, indent=4)}\n"
        )
        # json uses true/false/null; Python needs True/False/None
        body = (
            body.replace(": true", ": True")
            .replace(": false", ": False")
            .replace(": null", ": None")
        )
        (package_dir / "mcp_contracts.py").write_text(body, encoding="utf-8")
        print(f"{package}: {len(contracts)} tools")


if __name__ == "__main__":
    main()
