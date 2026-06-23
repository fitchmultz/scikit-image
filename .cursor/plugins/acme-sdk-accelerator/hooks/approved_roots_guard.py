#!/usr/bin/env python3
"""Minimal Cursor hook: keep agent context/actions inside approved roots."""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path
from typing import Any

PATHISH_KEYS = {
    "path",
    "file",
    "file_path",
    "filepath",
    "target_file",
    "target_path",
    "filename",
    "cwd",
}
ABS_PATH_RE = re.compile(r"(?:~|/Users/|/private/|/tmp/|/etc/|/var/|/opt/|/Library/)[^\s'\";|&<>]*")


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        return allow()

    workspace = workspace_root(event)
    config = load_config(workspace)
    if not config:
        return allow()

    roots = approved_roots(config, workspace)
    if not roots:
        return allow()

    denied: list[Path] = []
    hook = event.get("hook_event_name", "")

    if hook in {"beforeReadFile", "beforeTabFileRead"}:
        maybe_add_denied(denied, event.get("file_path"), roots, workspace)
    elif hook == "beforeShellExecution":
        for token in shell_path_candidates(str(event.get("command", ""))):
            maybe_add_denied(denied, token, roots, Path(event.get("cwd") or workspace))
    elif hook == "preToolUse":
        for value in collect_pathish(event.get("tool_input")):
            maybe_add_denied(denied, value, roots, Path(event.get("cwd") or workspace))

    if denied:
        paths = ", ".join(str(p) for p in sorted(set(denied)))
        msg = f"Blocked by Acme SDK Accelerator boundary. Path is outside approved roots: {paths}"
        print(json.dumps({"permission": "deny", "user_message": msg, "agent_message": msg}))
        return 0
    return allow()


def allow() -> int:
    print(json.dumps({"permission": "allow"}))
    return 0


def workspace_root(event: dict[str, Any]) -> Path:
    roots = event.get("workspace_roots") or []
    if roots:
        return Path(roots[0]).expanduser().resolve()
    env = os.environ.get("CURSOR_PROJECT_DIR") or os.getcwd()
    return Path(env).expanduser().resolve()


def load_config(workspace: Path) -> dict[str, Any] | None:
    for root in [workspace, *workspace.parents]:
        path = root / ".cursor" / "acme-sdk-accelerator" / "approved-roots.json"
        if path.exists():
            try:
                return json.loads(path.read_text())
            except json.JSONDecodeError:
                return None
    return None


def approved_roots(config: dict[str, Any], workspace: Path) -> list[Path]:
    roots = []
    for item in config.get("approvedRoots", []):
        path = Path(str(item)).expanduser()
        if not path.is_absolute():
            path = workspace / path
        roots.append(path.resolve())
    return roots


def inside(path: Path, roots: list[Path]) -> bool:
    return any(path == root or root in path.parents for root in roots)


def maybe_add_denied(denied: list[Path], value: Any, roots: list[Path], base: Path) -> None:
    if not isinstance(value, str) or not value.strip():
        return
    token = value.strip().strip("'\" ,:;()[]{}")
    if not looks_like_path(token):
        return
    path = Path(token).expanduser()
    if not path.is_absolute():
        path = base / path
    resolved = path.resolve(strict=False)
    if not inside(resolved, roots):
        denied.append(resolved)


def looks_like_path(value: str) -> bool:
    return (
        value.startswith(("/", "~", "../", "./"))
        or "/" in value
        or value.endswith((".py", ".md", ".rst", ".toml", ".json", ".txt", ".sh"))
    )


def shell_path_candidates(command: str) -> list[str]:
    candidates = ABS_PATH_RE.findall(command)
    try:
        candidates.extend(shlex.split(command))
    except ValueError:
        candidates.extend(command.split())
    return candidates


def collect_pathish(value: Any, key: str = "") -> list[str]:
    out: list[str] = []
    if isinstance(value, dict):
        for k, v in value.items():
            out.extend(collect_pathish(v, str(k)))
    elif isinstance(value, list):
        for item in value:
            out.extend(collect_pathish(item, key))
    elif isinstance(value, str) and (key.lower() in PATHISH_KEYS or looks_like_path(value)):
        out.append(value)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
