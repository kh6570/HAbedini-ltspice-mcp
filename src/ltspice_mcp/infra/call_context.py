# In the name of God, the Most Gracious, the Most Merciful
"""Per-call settings and the schematic hash supplied with a tool invocation."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from ltspice_mcp.infra.config import LTspiceSettings


@dataclass
class ContentHashContext:
    """Hash the current tool call may use when it writes one schematic."""

    digest: str | None
    path: Path | None


_SETTINGS: ContextVar[LTspiceSettings | None] = ContextVar("ltspice_settings", default=None)
_HASH: ContextVar[ContentHashContext | None] = ContextVar("ltspice_content_hash", default=None)


def current_settings() -> LTspiceSettings | None:
    """Return the settings bound for this tool call, if a handler set them."""

    return _SETTINGS.get()


def current_content_hash() -> ContentHashContext | None:
    """Return the hash context bound for this tool call."""

    return _HASH.get()


@contextmanager
def bind_settings(settings: LTspiceSettings) -> Iterator[None]:
    """Bind settings for the duration of one tool call."""

    token = _SETTINGS.set(settings)
    try:
        yield
    finally:
        _SETTINGS.reset(token)


@contextmanager
def bind_content_hash(digest: str | None, path: Path | None = None) -> Iterator[None]:
    """Bind the hash from the last read for saves made during this call."""

    token = _HASH.set(ContentHashContext(digest, None if path is None else path.resolve()))
    try:
        yield
    finally:
        _HASH.reset(token)
