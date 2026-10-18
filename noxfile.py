# In the name of God, the Most Gracious, the Most Merciful
"""Quality sessions for ltspice-mcp."""

from __future__ import annotations

import os
from pathlib import Path

import nox

nox.options.default_venv_backend = "venv"
nox.options.sessions = ["quality"]


def _core_checkout() -> Path | None:
    """Return a local mcp-app-core checkout, when one is available."""
    raw = os.environ.get("MCP_CORE_PATH", "").strip()
    if raw:
        candidate = Path(raw)
        if (candidate / "src" / "mcp_app_core" / "__init__.py").is_file():
            return candidate
        return None
    root = Path(__file__).resolve().parent
    parent = root.parent
    if not parent.is_dir():
        return None
    matches = [
        child
        for child in parent.iterdir()
        if child.is_dir()
        and child.resolve() != root
        and (child / "src" / "mcp_app_core" / "__init__.py").is_file()
    ]
    if len(matches) == 1:
        return matches[0]
    return None


def _prefer_local_core() -> Path | None:
    """Point the mcp-app-core dependency at a local checkout when one exists."""
    if os.environ.get("MCP_CORE_URI", "").strip():
        return _core_checkout()
    checkout = _core_checkout()
    if checkout is not None:
        os.environ["MCP_CORE_URI"] = checkout.resolve().as_uri()
    return checkout


def _install_dev(session: nox.Session) -> None:
    checkout = _prefer_local_core()
    session.install(".[dev]")
    if checkout is not None:
        session.install("-e", str(checkout), "--no-deps")


@nox.session
def lint(session: nox.Session) -> None:
    """Run ruff."""

    session.install("ruff==0.15.12")
    session.run("ruff", "check", "src", "tests", "scripts")
    session.run("ruff", "format", "--check", "src", "tests", "scripts")


@nox.session
def mypy(session: nox.Session) -> None:
    """Type-check the package."""

    _install_dev(session)
    session.run("mypy", "--strict", "src/ltspice_mcp")


@nox.session
def tests(session: nox.Session) -> None:
    """Run tests that do not need LTspice."""

    _install_dev(session)
    session.run("pytest", "-m", "not integration")


@nox.session
def integration(session: nox.Session) -> None:
    """Run tests that need LTspice on PATH or in a default install location."""

    _install_dev(session)
    session.run("pytest", "-m", "integration")


@nox.session
def quality(session: nox.Session) -> None:
    """Lint, type-check, and run unit tests."""

    _install_dev(session)
    session.run("ruff", "check", "src", "tests", "scripts")
    session.run("mypy", "--strict", "src/ltspice_mcp")
    session.run("pytest", "-m", "not integration")
