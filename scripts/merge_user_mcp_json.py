# In the name of God, the Most Gracious, the Most Merciful
"""Merge one MCP server entry into a user-level mcp.json file.

Existing servers, including qspice, are left in place. Only the named server
entry is replaced.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_EXPECTED_ARG_COUNT = 5


def main() -> int:
    if len(sys.argv) != _EXPECTED_ARG_COUNT:
        print(
            "usage: merge_user_mcp_json.py <config_path> <root_key> "
            "<server_name> <entry_json_path>",
            file=sys.stderr,
        )
        return 2

    config_path = Path(sys.argv[1])
    root_key = sys.argv[2]
    server_name = sys.argv[3]
    entry_path = Path(sys.argv[4])

    entry: dict[str, Any] = json.loads(entry_path.read_text(encoding="utf-8"))
    data: dict[str, Any] = {}
    if config_path.is_file():
        raw = config_path.read_text(encoding="utf-8-sig").strip()
        if raw:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                data = parsed

    servers = data.get(root_key)
    if not isinstance(servers, dict):
        servers = {}
        data[root_key] = servers

    servers[server_name] = entry
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"updated {config_path} ({root_key}.{server_name})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
