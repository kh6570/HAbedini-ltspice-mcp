# In the name of God, the Most Gracious, the Most Merciful
"""Package entry point."""

from __future__ import annotations

import argparse
import json
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from ltspice_mcp import __version__
from ltspice_mcp.infra import build_settings, configure_logging
from ltspice_mcp.infra.bootstrap import describe_environment_readiness
from ltspice_mcp.mcp import run


def _package_version() -> str:
    try:
        return version("ltspice-mcp")
    except PackageNotFoundError:
        return __version__


def _configure_stdio_utf8() -> None:
    """Prefer UTF-8 stdio on Windows so tool output with Unicode does not crash."""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                continue


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Each configuration flag mirrors an ``LTSPICE_*`` environment variable.
    The CLI value wins.
    """

    parser = argparse.ArgumentParser(description="LTspice MCP server")
    parser.add_argument(
        "--version",
        action="version",
        version=f"ltspice-mcp {_package_version()}",
    )
    parser.add_argument("--transport", choices=("stdio", "sse"), default=None)
    parser.add_argument(
        "--session-mode",
        choices=("cold", "auto"),
        default=None,
        help="cold always starts a fresh batch run. auto is accepted and behaves as cold.",
    )
    parser.add_argument("--ltspice-exe", type=Path, default=None)
    parser.add_argument("--workspace-root", type=Path, default=None)
    parser.add_argument("--log-folder", type=Path, default=None)
    parser.add_argument("--recipe-path", type=Path, default=None)
    parser.add_argument(
        "--active-profiles",
        default=None,
        help="Comma-separated profiles. Use default,extended to load hidden groups.",
    )
    parser.add_argument(
        "--window-sync",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Attach saves to an LTspice window the user already opened.",
    )
    parser.add_argument(
        "--log-level",
        choices=("debug", "info", "warning", "error"),
        default=None,
    )
    parser.add_argument(
        "--describe",
        action="store_true",
        help="Print the bootstrap summary as JSON and exit successfully.",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Print an environment readiness report as JSON and exit.",
    )
    return parser


def main() -> None:
    """Parse CLI arguments and run the MCP server."""

    parser = build_arg_parser()
    args = parser.parse_args()
    _configure_stdio_utf8()
    settings = build_settings(
        transport=args.transport,
        exe=args.ltspice_exe,
        workspace_root=args.workspace_root,
        log_level=args.log_level,
        log_folder=args.log_folder,
        recipe_path=args.recipe_path,
        session_mode=args.session_mode,
        active_profiles=args.active_profiles,
        window_sync=args.window_sync,
    )
    configure_logging(settings.log_level, log_folder=settings.log_folder)

    if args.setup:
        print(json.dumps(describe_environment_readiness(settings), indent=2))
        raise SystemExit(0)

    if settings.transport == "sse" and not settings.enable_sse:
        print(
            "ERROR: the sse transport is gated behind LTSPICE_ENABLE_SSE=true.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    raise SystemExit(run(settings=settings, describe=args.describe))


if __name__ == "__main__":
    main()
