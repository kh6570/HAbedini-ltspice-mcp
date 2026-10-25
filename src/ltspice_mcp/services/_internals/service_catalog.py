# In the name of God, the Most Gracious, the Most Merciful
"""Service discovery for LTspice. The walker lives in mcp-app-core."""

from __future__ import annotations

from dataclasses import replace
from functools import cache
from importlib import import_module
from typing import TYPE_CHECKING

from mcp_app_core.catalog import ServiceSpec, enrich_spec, profile_for_area
from mcp_app_core.catalog import discover_package_specs as _discover_package_specs
from mcp_app_core.catalog import load_contracts as _load_contracts
from mcp_app_core.catalog import resolve_service_module as _resolve_service_module

if TYPE_CHECKING:
    from types import ModuleType

_SERVICE_PACKAGE_ORDER: tuple[str, ...] = (
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
_PACKAGES = tuple(f"ltspice_mcp.services.{name}" for name in _SERVICE_PACKAGE_ORDER)
_EXTENDED_PACKAGE_AREA = {
    "batch": "batch",
    "remote": "remote",
    "live_gui": "live_gui",
    "topology": "topology_ingest",
}
EXTENDED_GROUP_PACKAGES = {
    "batch": "batch",
    "remote": "remote",
    "live_gui": "live_gui",
    "topology_ingest": "topology",
}


@cache
def build_mcp_contract_catalog() -> dict[str, dict[str, object]]:
    """Build the full MCP contract catalog."""

    catalog: dict[str, dict[str, object]] = {}
    for package_name in _PACKAGES:
        catalog.update(_load_contracts(package_name))
    catalog.update(_load_contracts("ltspice_mcp.services._internals"))
    return catalog


def _with_area_profile(
    package_name: str, specs: tuple[ServiceSpec, ...]
) -> tuple[ServiceSpec, ...]:
    area = _EXTENDED_PACKAGE_AREA.get(package_name)
    if area is None:
        return specs
    profile = profile_for_area(area)
    return tuple(replace(spec, profile=profile) for spec in specs)


@cache
def discover_package_service_specs(package_name: str) -> tuple[ServiceSpec, ...]:
    """Return service specs found under one package."""

    discovered = _discover_package_specs(f"ltspice_mcp.services.{package_name}")
    return _with_area_profile(package_name, discovered)


@cache
def build_service_spec_catalog(
    extra_specs: tuple[ServiceSpec, ...] = (),
) -> tuple[ServiceSpec, ...]:
    """Build the full service catalog."""

    contracts = build_mcp_contract_catalog()
    catalog = [enrich_spec(spec, contracts.get(spec.name)) for spec in extra_specs]
    for package_name in _SERVICE_PACKAGE_ORDER:
        catalog.extend(discover_package_service_specs(package_name))
    return tuple(catalog)


def resolve_service_module(service_name: str) -> ModuleType:
    """Import the module that defines one tool."""

    return _resolve_service_module(_PACKAGES, service_name)


@cache
def build_service_callable_catalog() -> dict[str, object]:
    """Map implemented tool names to callables."""

    catalog: dict[str, object] = {}
    for spec in build_service_spec_catalog():
        if spec.phase != "implemented":
            continue
        module = resolve_service_module(spec.name)
        service_fn = getattr(module, spec.name, None)
        if not callable(service_fn) and module.__package__ is not None:
            operations = import_module(f"{module.__package__}.operations")
            service_fn = getattr(operations, spec.name, None)
            if not callable(service_fn):
                service_fn = getattr(operations, f"{spec.name}_service", None)
        if callable(service_fn):
            catalog[spec.name] = service_fn
    return catalog
