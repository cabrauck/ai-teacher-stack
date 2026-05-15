from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

WIKI_MCP_TYPE = "project_memories"


def _api_url(base_url: str, path: str) -> str:
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def _read_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    timeout_seconds: float = 4.0,
) -> dict[str, Any]:
    data = None
    headers: dict[str, str] = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url, data=data, headers=headers, method=method)
    with urlopen(request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8", errors="replace")

    if not body:
        return {}
    return json.loads(body)


def _error_result(exc: Exception, *, url: str) -> dict[str, Any]:
    if isinstance(exc, HTTPError):
        detail = f"HTTP {exc.code}"
        try:
            payload = exc.read().decode("utf-8", errors="replace")
            if payload:
                detail = payload
        except OSError:
            pass
        return {"status": "error", "url": url, "detail": detail}
    if isinstance(exc, URLError):
        return {"status": "error", "url": url, "detail": str(exc.reason)}
    return {"status": "error", "url": url, "detail": str(exc)}


def _get_json(
    base_url: str,
    path: str,
    *,
    timeout_seconds: float = 4.0,
) -> dict[str, Any]:
    url = _api_url(base_url, path)
    try:
        return _read_json(url, timeout_seconds=timeout_seconds)
    except Exception as exc:
        return _error_result(exc, url=url)


def _post_json(
    base_url: str,
    path: str,
    payload: dict[str, Any],
    *,
    timeout_seconds: float = 8.0,
) -> dict[str, Any]:
    url = _api_url(base_url, path)
    try:
        return _read_json(
            url,
            method="POST",
            payload=payload,
            timeout_seconds=timeout_seconds,
        )
    except Exception as exc:
        return _error_result(exc, url=url)


def _find_by_name(items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for item in items:
        if item.get("name") == name:
            return item
    return None


def _document_count(stats: dict[str, Any], documents: dict[str, Any]) -> int:
    for key in ("total_documents", "document_count", "documents"):
        value = stats.get(key)
        if isinstance(value, int):
            return value
    docs = documents.get("documents")
    return len(docs) if isinstance(docs, list) else 0


def _chunk_count(stats: dict[str, Any]) -> int:
    for key in ("total_chunks", "chunk_count", "chunks"):
        value = stats.get(key)
        if isinstance(value, int):
            return value
    return 0


def _source_path(source: dict[str, Any]) -> str | None:
    metadata = source.get("metadata")
    if isinstance(metadata, dict):
        for key in ("filename", "path", "source", "file_path"):
            value = metadata.get(key)
            if isinstance(value, str) and value:
                return value
    for key in ("filename", "path", "doc_id"):
        value = source.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def inspect_claude_os_runtime(
    claude_os_url: str,
    *,
    project_name: str,
    wiki_kb_name: str,
    wiki_mcp_type: str = WIKI_MCP_TYPE,
    timeout_seconds: float = 4.0,
) -> dict[str, Any]:
    projects_payload = _get_json(
        claude_os_url,
        "/api/projects",
        timeout_seconds=timeout_seconds,
    )
    if projects_payload.get("status") == "error":
        return {
            "status": "error",
            "detail": projects_payload.get("detail"),
            "project_name": project_name,
            "wiki_kb_name": wiki_kb_name,
        }

    projects = projects_payload.get("projects", [])
    project = _find_by_name(projects if isinstance(projects, list) else [], project_name)

    kbs_payload = _get_json(claude_os_url, "/api/kb", timeout_seconds=timeout_seconds)
    kbs = kbs_payload.get("knowledge_bases", [])
    knowledge_bases = kbs if isinstance(kbs, list) else []
    wiki_kb = _find_by_name(knowledge_bases, wiki_kb_name)

    mcps_payload: dict[str, Any] = {}
    folders_payload: dict[str, Any] = {}
    hooks_payload: dict[str, Any] = {}
    if project and isinstance(project.get("id"), int):
        project_id = project["id"]
        mcps_payload = _get_json(
            claude_os_url,
            f"/api/projects/{project_id}/mcps",
            timeout_seconds=timeout_seconds,
        )
        folders_payload = _get_json(
            claude_os_url,
            f"/api/projects/{project_id}/folders",
            timeout_seconds=timeout_seconds,
        )
        hooks_payload = _get_json(
            claude_os_url,
            f"/api/projects/{project_id}/hooks",
            timeout_seconds=timeout_seconds,
        )

    encoded_kb = quote(wiki_kb_name, safe="")
    stats = _get_json(
        claude_os_url,
        f"/api/kb/{encoded_kb}/stats",
        timeout_seconds=timeout_seconds,
    )
    documents = _get_json(
        claude_os_url,
        f"/api/kb/{encoded_kb}/documents",
        timeout_seconds=timeout_seconds,
    )
    jobs = _get_json(claude_os_url, "/api/jobs", timeout_seconds=timeout_seconds)
    services = _get_json(
        claude_os_url,
        "/api/services/status",
        timeout_seconds=timeout_seconds,
    )

    errors = []
    if not project:
        errors.append("project missing")
    if not wiki_kb:
        errors.append("wiki knowledge base missing")
    if stats.get("status") == "error":
        errors.append("wiki KB stats unavailable")
    if documents.get("status") == "error":
        errors.append("wiki KB documents unavailable")

    doc_count = _document_count(stats, documents)
    chunks = _chunk_count(stats)
    embedding_coverage = {
        "status": "ok" if doc_count > 0 and chunks > 0 else "degraded",
        "document_count": doc_count,
        "chunk_count": chunks,
        "detail": (
            "No indexed wiki documents or chunks yet."
            if chunks == 0
            else "Indexed chunks present."
        ),
    }

    hooks_status = hooks_payload.get("status", {})
    hooks = hooks_status.get("hooks", {}) if isinstance(hooks_status, dict) else {}
    wiki_hook = hooks.get(wiki_mcp_type, {}) if isinstance(hooks, dict) else {}

    return {
        "status": "ok" if not errors else "degraded",
        "detail": "; ".join(errors) if errors else "Claude-OS project and wiki KB are configured.",
        "project": project,
        "knowledge_base_count": len(knowledge_bases),
        "wiki_kb": wiki_kb,
        "wiki_kb_name": wiki_kb_name,
        "wiki_mcp_type": wiki_mcp_type,
        "mcps": mcps_payload.get("mcps", []),
        "folders": folders_payload.get("folders", {}),
        "wiki_hook": wiki_hook,
        "stats": stats,
        "documents": documents.get("documents", []),
        "document_count": doc_count,
        "chunk_count": chunks,
        "embedding_coverage": embedding_coverage,
        "jobs": jobs.get("jobs", []),
        "services": services.get("services", []),
        "services_summary": services.get("summary", {}),
    }


def sync_claude_os_memory(
    claude_os_url: str,
    *,
    project_name: str,
    wiki_mcp_type: str = WIKI_MCP_TYPE,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    projects_payload = _get_json(
        claude_os_url,
        "/api/projects",
        timeout_seconds=timeout_seconds,
    )
    if projects_payload.get("status") == "error":
        return {
            "status": "error",
            "detail": projects_payload.get("detail"),
            "project_name": project_name,
            "mcp_type": wiki_mcp_type,
        }

    projects = projects_payload.get("projects", [])
    project = _find_by_name(projects if isinstance(projects, list) else [], project_name)
    if not project or not isinstance(project.get("id"), int):
        return {
            "status": "error",
            "detail": f"Claude-OS project not found: {project_name}",
            "project_name": project_name,
            "mcp_type": wiki_mcp_type,
        }

    result = _post_json(
        claude_os_url,
        f"/api/projects/{project['id']}/hooks/sync",
        {"mcp_type": wiki_mcp_type},
        timeout_seconds=timeout_seconds,
    )
    if result.get("status") == "error":
        return {
            "status": "error",
            "project_id": project["id"],
            "project_name": project_name,
            "mcp_type": wiki_mcp_type,
            "detail": result.get("detail"),
        }

    return {
        "status": "ok",
        "project_id": project["id"],
        "project_name": project_name,
        "mcp_type": wiki_mcp_type,
        "sync": result,
    }


def search_claude_os_memory(
    claude_os_url: str,
    *,
    wiki_kb_name: str,
    query: str,
    use_hybrid: bool = False,
    use_rerank: bool = False,
    use_agentic: bool = False,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    if not query.strip():
        raise ValueError("query must not be empty")

    encoded_kb = quote(wiki_kb_name, safe="")
    result = _post_json(
        claude_os_url,
        f"/api/kb/{encoded_kb}/chat",
        {
            "query": query,
            "use_hybrid": use_hybrid,
            "use_rerank": use_rerank,
            "use_agentic": use_agentic,
        },
        timeout_seconds=timeout_seconds,
    )
    if result.get("status") == "error":
        return {
            "status": "unavailable",
            "kb_name": wiki_kb_name,
            "query": query,
            "detail": result.get("detail"),
            "modes": {
                "hybrid": use_hybrid,
                "rerank": use_rerank,
                "agentic": use_agentic,
            },
            "sources": [],
        }

    raw_sources = result.get("sources", [])
    sources: list[dict[str, Any]] = []
    if isinstance(raw_sources, list):
        for source in raw_sources:
            if not isinstance(source, dict):
                continue
            sources.append(
                {
                    "path": _source_path(source),
                    "score": source.get("score"),
                    "metadata": source.get("metadata", {}),
                    "excerpt": source.get("content") or source.get("text"),
                }
            )

    return {
        "status": "ok",
        "kb_name": wiki_kb_name,
        "query": query,
        "answer": result.get("answer") or result.get("response") or "",
        "sources": sources,
        "modes": {
            "hybrid": use_hybrid,
            "rerank": use_rerank,
            "agentic": use_agentic,
        },
        "note": (
            "Local Claude-OS memory was queried. Cite returned local wiki paths "
            "or document names when using these results."
        ),
        "raw": result,
    }
