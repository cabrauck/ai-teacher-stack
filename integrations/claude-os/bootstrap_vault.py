#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


MCP_TYPES = ("knowledge_docs", "project_profile", "project_index", "project_memories")
DEFAULT_PROJECT_NAME = "ai-teacher-stack"
DEFAULT_WORKSPACE_PATH = "/workspace"
DEFAULT_WIKI_PATH = "/workspace/vault/Wiki"
DEFAULT_WIKI_KB_NAME = "ai-teacher-stack-wiki"
DEFAULT_WIKI_MCP_TYPE = "project_memories"

TEACHER_MEMORY_NOTE = (
    "Hinweis: Diese Long-Term-Memory-Notiz ist ein lokal gespeicherter Entwurf. "
    "Vor Wiederverwendung fachlich, didaktisch und datenschutzrechtlich pruefen."
)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().casefold() in {"1", "true", "yes", "on"}


def _utc_stamp() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()


def _ensure_wiki_files(wiki_path: Path) -> None:
    wiki_path.mkdir(parents=True, exist_ok=True)

    index_path = wiki_path / "index.md"
    if not index_path.exists():
        index_path.write_text(
            "\n".join(
                [
                    "# Long-Term Memory Index",
                    "",
                    TEACHER_MEMORY_NOTE,
                    "",
                    "## Wiki-Seiten",
                    "",
                    "_Noch keine Wiki-Seiten._",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    log_path = wiki_path / "log.md"
    if not log_path.exists():
        log_path.write_text("# Long-Term Memory Log\n\n", encoding="utf-8")

    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"- {_utc_stamp()} | claude_os_bootstrap | `Wiki` | "
            "Claude-OS KB bootstrap configured\n"
        )


def _find_project(db_manager, *, name: str, path: str) -> dict | None:
    for project in db_manager.list_projects():
        if project["name"] == name or project["path"] == path:
            return project
    return None


def _collection_by_name(db_manager, name: str) -> dict | None:
    for collection in db_manager.list_collections():
        if collection["name"] == name:
            return collection
    return None


def _collection_by_id(db_manager, kb_id: int) -> dict | None:
    for collection in db_manager.list_collections():
        if collection["id"] == kb_id:
            return collection
    return None


def _ensure_collection(db_manager, *, name: str, description: str) -> dict:
    from app.core.kb_types import KBType

    existing = _collection_by_name(db_manager, name)
    if existing:
        return existing

    return db_manager.create_collection(
        name=name,
        kb_type=KBType.GENERIC,
        description=description,
        tags=["ai-teacher-stack", "obsidian", "privacy-checked"],
    )


def _ensure_project(db_manager, *, name: str, path: str) -> dict:
    existing = _find_project(db_manager, name=name, path=path)
    if existing:
        return existing

    return db_manager.create_project(
        name=name,
        path=path,
        description="ai-teacher-stack local teacher workspace",
        metadata={"bootstrap": "ai-teacher-stack"},
    )


def _ensure_project_mcp(
    db_manager,
    *,
    project_id: int,
    project_name: str,
    mcp_type: str,
    kb_name: str,
) -> dict:
    assigned = db_manager.get_project_kbs(project_id)
    if mcp_type in assigned:
        existing = _collection_by_id(db_manager, assigned[mcp_type])
        if existing:
            return existing

    collection = _ensure_collection(
        db_manager,
        name=kb_name,
        description=f"{mcp_type.replace('_', ' ').title()} for {project_name}",
    )
    db_manager.assign_kb_to_project(project_id, collection["id"], mcp_type)
    return collection


def _model_matches(actual: str, wanted: str) -> bool:
    if actual == wanted:
        return True
    if ":" not in wanted and actual.split(":", 1)[0] == wanted:
        return True
    return False


def _ollama_embedding_model_available(base_url: str, model_name: str) -> bool:
    url = base_url.rstrip("/") + "/api/tags"
    try:
        with urlopen(url, timeout=2) as response:
            if response.status != 200:
                return False
            payload = json.load(response)
    except (OSError, URLError):
        return False

    models = payload.get("models", [])
    names = [str(model.get("name", "")) for model in models if isinstance(model, dict)]
    return any(_model_matches(name, model_name) for name in names)


def bootstrap() -> dict:
    from app.core.hooks import get_project_hook
    from app.core.sqlite_manager import get_sqlite_manager

    project_name = os.getenv("CLAUDE_OS_PROJECT_NAME", DEFAULT_PROJECT_NAME)
    workspace_path = os.getenv("CLAUDE_OS_WORKSPACE_PATH", DEFAULT_WORKSPACE_PATH)
    wiki_path = Path(os.getenv("CLAUDE_OS_WIKI_PATH", DEFAULT_WIKI_PATH))
    wiki_kb_name = os.getenv("CLAUDE_OS_WIKI_KB_NAME", DEFAULT_WIKI_KB_NAME)
    wiki_mcp_type = os.getenv("CLAUDE_OS_WIKI_MCP_TYPE", DEFAULT_WIKI_MCP_TYPE)

    if wiki_mcp_type not in MCP_TYPES:
        raise ValueError(f"Invalid CLAUDE_OS_WIKI_MCP_TYPE: {wiki_mcp_type}")

    _ensure_wiki_files(wiki_path)

    db_manager = get_sqlite_manager()
    project = _ensure_project(db_manager, name=project_name, path=workspace_path)

    mcps: dict[str, str] = {}
    for mcp_type in MCP_TYPES:
        kb_name = wiki_kb_name if mcp_type == wiki_mcp_type else f"{project_name}-{mcp_type}"
        collection = _ensure_project_mcp(
            db_manager,
            project_id=project["id"],
            project_name=project_name,
            mcp_type=mcp_type,
            kb_name=kb_name,
        )
        mcps[mcp_type] = collection["name"]

    db_manager.set_kb_folder(
        project["id"],
        wiki_mcp_type,
        str(wiki_path),
        auto_sync=True,
    )

    hook = get_project_hook(project["id"], db_manager)
    hook.enable_kb_autosync(wiki_mcp_type, str(wiki_path), [".md", ".markdown"])

    sync_result: dict[str, object] = {"status": "skipped", "reason": "sync disabled"}
    if _env_bool("CLAUDE_OS_BOOTSTRAP_SYNC", True):
        ollama_host = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
        embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
        if _ollama_embedding_model_available(ollama_host, embed_model):
            sync_result = hook.sync_kb_folder(wiki_mcp_type)
        else:
            sync_result = {
                "status": "skipped",
                "reason": "ollama embedding model unavailable",
                "model": embed_model,
            }

    return {
        "project_id": project["id"],
        "project_name": project["name"],
        "workspace_path": workspace_path,
        "wiki_path": str(wiki_path),
        "wiki_mcp_type": wiki_mcp_type,
        "wiki_kb_name": mcps[wiki_mcp_type],
        "sync_result": sync_result,
    }


def main() -> int:
    result = bootstrap()
    print(f"Claude-OS vault bootstrap complete: {result}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Claude-OS vault bootstrap failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
