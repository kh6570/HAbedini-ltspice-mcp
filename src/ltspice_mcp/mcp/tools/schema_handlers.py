# In the name of God, the Most Gracious, the Most Merciful
"""Adapt generic handlers to FastMCP signatures."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ltspice_mcp.mcp.tool_registry import ToolDefinition

ToolHandler = Callable[..., dict[str, object]]


def expose_tool_schema(handler: ToolHandler, tool: ToolDefinition) -> ToolHandler:
    """Give a handler the keyword signature that its JSON schema advertises."""

    schema = tool.input_schema
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        properties = {}
    required = schema.get("required", [])
    required_names = {str(item) for item in required} if isinstance(required, list) else set()
    parameters: list[inspect.Parameter] = []
    for name in properties:
        default: object = inspect.Parameter.empty if name in required_names else None
        parameters.append(
            inspect.Parameter(
                name, inspect.Parameter.KEYWORD_ONLY, default=default, annotation=object
            )
        )
    signature = inspect.Signature(parameters, return_annotation=dict[str, object])

    def schema_handler(**kwargs: object) -> dict[str, object]:
        provided = {name: value for name, value in kwargs.items() if value is not None}
        return handler(**provided)

    schema_handler.__name__ = tool.name
    schema_handler.__doc__ = tool.description
    schema_handler.__signature__ = signature  # type: ignore[attr-defined]
    schema_handler.__annotations__ = {parameter.name: object for parameter in parameters}
    schema_handler.__annotations__["return"] = dict[str, object]
    return schema_handler
