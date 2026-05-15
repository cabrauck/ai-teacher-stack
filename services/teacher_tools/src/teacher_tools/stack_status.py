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


def _public_url(host: str, port: int, path: str = "") -> str:
    base = f"http://{host}:{port}"
    if not path:
        return base
    return f"{base}/{path.lstrip('/')}"


def inspect_http_service(
    service_url: str,
    *,
    health_path: str = "/",
    timeout_seconds: float = 2.0,
) -> dict[str, Any]:
    health_url = urljoin(service_url.rstrip("/") + "/", health_path.lstrip("/"))
    result: dict[str, Any] = {
        "status": "error",
        "url": service_url,
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


def inspect_claude_os_service(
    claude_os_url: str,
    *,
    timeout_seconds: float = 2.0,
) -> dict[str, Any]:
    return inspect_http_service(
        claude_os_url,
        health_path="/health",
        timeout_seconds=timeout_seconds,
    )


def inspect_librechat_service(
    librechat_url: str,
    *,
    timeout_seconds: float = 2.0,
) -> dict[str, Any]:
    return inspect_http_service(
        librechat_url,
        health_path="/",
        timeout_seconds=timeout_seconds,
    )


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
    librechat_url: str,
    public_host: str,
    host_librechat_port: int,
    host_teacher_tools_port: int,
    host_claude_os_port: int,
) -> dict[str, Any]:
    teacher_tools = {"status": "ok"}
    claude_os = inspect_claude_os_service(claude_os_url)
    librechat = inspect_librechat_service(librechat_url)
    vault = inspect_vault_structure(vault_root)
    exports = inspect_export_root(export_root)
    memory = inspect_memory_bootstrap(vault_root)

    checks = {
        "teacher_tools": teacher_tools,
        "claude_os": claude_os,
        "librechat": librechat,
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
            "librechat": librechat,
        },
        "storage": {
            "vault": vault,
            "exports": exports,
            "memory": memory,
        },
        "urls": {
            "librechat": _public_url(public_host, host_librechat_port),
            "teacher_tools_api": _public_url(public_host, host_teacher_tools_port),
            "teacher_tools_status": _public_url(public_host, host_teacher_tools_port, "/status"),
            "claude_os": _public_url(public_host, host_claude_os_port),
        },
    }
