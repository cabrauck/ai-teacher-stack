from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import urlopen


def _now_iso() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _path_matches_expected_type(path: Path) -> bool:
    if path.suffix:
        return path.is_file()
    return path.is_dir()


def inspect_claude_os_service(
    claude_os_url: str,
    *,
    timeout_seconds: float = 2.0,
) -> dict[str, Any]:
    health_url = urljoin(claude_os_url.rstrip("/") + "/", "health")
    result: dict[str, Any] = {
        "status": "error",
        "url": claude_os_url,
        "health_url": health_url,
        "reachable": False,
    }
    try:
        with urlopen(health_url, timeout=timeout_seconds) as response:
            status_code = response.getcode()
            payload = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        result["detail"] = f"HTTP {exc.code}"
        return result
    except URLError as exc:
        result["detail"] = str(exc.reason)
        return result

    result["http_status"] = status_code
    result["reachable"] = 200 <= status_code < 300
    if result["reachable"]:
        result["status"] = "ok"

    if payload:
        try:
            result["response"] = json.loads(payload)
        except json.JSONDecodeError:
            result["response_text"] = payload
    return result


def inspect_vault_structure(vault_root: Path) -> dict[str, Any]:
    required = {
        "Sources": vault_root / "Sources",
        "Wiki": vault_root / "Wiki",
        "Wiki/index.md": vault_root / "Wiki" / "index.md",
        "Wiki/log.md": vault_root / "Wiki" / "log.md",
    }
    missing = [
        name
        for name, path in required.items()
        if not _path_matches_expected_type(path)
    ]
    status = "ok" if not missing else "error"
    return {
        "status": status,
        "path": vault_root.as_posix(),
        "exists": vault_root.exists(),
        "missing": missing,
    }


def inspect_export_root(export_root: Path) -> dict[str, Any]:
    if not export_root.exists():
        return {
            "status": "error",
            "path": export_root.as_posix(),
            "exists": False,
            "document_files": 0,
            "is_empty": True,
        }

    files = [
        path
        for path in export_root.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]
    return {
        "status": "ok",
        "path": export_root.as_posix(),
        "exists": True,
        "document_files": len(files),
        "is_empty": len(files) == 0,
    }


def inspect_memory_bootstrap(vault_root: Path) -> dict[str, Any]:
    wiki_root = vault_root / "Wiki"
    index_path = wiki_root / "index.md"
    log_path = wiki_root / "log.md"
    missing = [
        path_name
        for path_name, path in {
            "Wiki": wiki_root,
            "Wiki/index.md": index_path,
            "Wiki/log.md": log_path,
        }.items()
        if not _path_matches_expected_type(path)
    ]
    wiki_pages = [
        path
        for path in wiki_root.glob("*.md")
        if path.name not in {"index.md", "log.md"}
    ] if wiki_root.is_dir() else []
    return {
        "status": "ok" if not missing else "error",
        "index_path": _relative(index_path, vault_root),
        "log_path": _relative(log_path, vault_root),
        "missing": missing,
        "wiki_pages": len(wiki_pages),
    }


def build_stack_status(
    *,
    vault_root: Path,
    export_root: Path,
    claude_os_url: str,
) -> dict[str, Any]:
    teacher_tools = {"status": "ok"}
    claude_os = inspect_claude_os_service(claude_os_url)
    vault = inspect_vault_structure(vault_root)
    exports = inspect_export_root(export_root)
    memory = inspect_memory_bootstrap(vault_root)

    checks = {
        "teacher_tools": teacher_tools,
        "claude_os": claude_os,
        "vault": vault,
        "exports": exports,
        "memory": memory,
    }
    ready = all(section["status"] == "ok" for section in checks.values())
    return {
        "status": "ok" if ready else "degraded",
        "ready": ready,
        "generated_at": _now_iso(),
        "services": {
            "teacher_tools": teacher_tools,
            "claude_os": claude_os,
        },
        "storage": {
            "vault": vault,
            "exports": exports,
            "memory": memory,
        },
        "urls": {
            "teacher_tools_api": "http://localhost:8010",
            "teacher_tools_status": "http://localhost:8010/status",
            "claude_os": "http://localhost:8051",
        },
    }
