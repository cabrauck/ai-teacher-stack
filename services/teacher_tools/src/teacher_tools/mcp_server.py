from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from teacher_tools.claude_os import (
    inspect_claude_os_runtime,
    search_claude_os_memory,
    sync_claude_os_memory,
)
from teacher_tools.curriculum import load_curriculum_records, search_curriculum
from teacher_tools.documents import export_lesson_docx, lesson_to_markdown
from teacher_tools.lessons import generate_lesson_plan
from teacher_tools.memory import (
    create_source_note,
    lint_memory_wiki,
    memory_schema_markdown,
    promote_source_to_wiki,
    read_memory_index,
    write_wiki_page,
)
from teacher_tools.models import LessonRequest
from teacher_tools.schriftwesen import (
    WeeklyPlanRequest,
    generate_weekly_plan,
    schriftwesen_to_markdown,
)
from teacher_tools.settings import settings
from teacher_tools.stack_status import build_stack_status


def _records() -> list[dict[str, Any]]:
    return [
        record.model_dump(mode="json")
        for record in load_curriculum_records(settings.curriculum_root)
    ]


def search_curriculum_records(query: str = "") -> dict[str, Any]:
    records = load_curriculum_records(settings.curriculum_root)
    return {
        "query": query,
        "results": [
            record.model_dump(mode="json")
            for record in search_curriculum(records, query)
        ],
    }


def create_lesson_markdown(
    subject: str,
    topic: str,
    grade_band: str = "3/4",
    duration_minutes: int = 45,
) -> dict[str, str]:
    records = load_curriculum_records(settings.curriculum_root)
    lesson = generate_lesson_plan(
        LessonRequest(
            subject=subject,
            grade_band=grade_band,
            topic=topic,
            duration_minutes=duration_minutes,
        ),
        records,
    )
    return {"markdown": lesson_to_markdown(lesson)}


def export_lesson_docx_file(
    subject: str,
    topic: str,
    grade_band: str = "3/4",
    duration_minutes: int = 45,
    filename: str | None = None,
) -> dict[str, str]:
    records = load_curriculum_records(settings.curriculum_root)
    lesson = generate_lesson_plan(
        LessonRequest(
            subject=subject,
            grade_band=grade_band,
            topic=topic,
            duration_minutes=duration_minutes,
        ),
        records,
    )
    path = export_lesson_docx(lesson, settings.export_root, filename=filename)
    return {"path": path.as_posix()}


def create_weekly_plan_markdown(
    woche: str,
    klasse: str,
    themen: list[str] | None = None,
) -> dict[str, str]:
    plan = generate_weekly_plan(
        WeeklyPlanRequest(
            woche=woche,
            klasse=klasse,
            themen=themen or [],
            personenbezogene_daten=False,
        )
    )
    return {"markdown": schriftwesen_to_markdown(plan)}


def create_memory_source_note(
    title: str,
    body: str,
    source_type: str = "note",
    tags: list[str] | None = None,
) -> dict[str, str]:
    result = create_source_note(
        settings.vault_root,
        title=title,
        body=body,
        source_type=source_type,
        tags=tags or [],
    )
    return {
        "title": result.title,
        "path": result.relative_path,
        "privacy_status": result.privacy_status,
    }


def write_memory_wiki_page(
    title: str,
    body: str,
    tags: list[str] | None = None,
    source_path: str | None = None,
) -> dict[str, str]:
    result = write_wiki_page(
        settings.vault_root,
        title=title,
        body=body,
        tags=tags or [],
        source_path=source_path,
    )
    return {
        "title": result.title,
        "path": result.relative_path,
        "privacy_status": result.privacy_status,
    }


def promote_memory_source_note(
    source_path: str,
    title: str | None = None,
    summary: str | None = None,
    tags: list[str] | None = None,
) -> dict[str, str]:
    result = promote_source_to_wiki(
        settings.vault_root,
        source_path=source_path,
        title=title,
        summary=summary,
        tags=tags or [],
    )
    return {
        "source_path": result.source_path,
        "title": result.wiki.title,
        "path": result.wiki.relative_path,
        "privacy_status": result.wiki.privacy_status,
    }


def list_memory_wiki_pages() -> dict[str, Any]:
    wiki_root = settings.vault_root / "Wiki"
    pages = []
    if wiki_root.is_dir():
        for path in sorted(wiki_root.glob("*.md")):
            if path.name in {"index.md", "log.md"}:
                continue
            title = path.stem
            try:
                for line in path.read_text(encoding="utf-8").splitlines():
                    if line.startswith("# "):
                        title = line.removeprefix("# ").strip()
                        break
            except OSError:
                title = path.stem
            pages.append(
                {
                    "title": title,
                    "path": path.relative_to(settings.vault_root).as_posix(),
                    "filename": path.name,
                }
            )

    return {
        "count": len(pages),
        "pages": pages,
        "note": "Nur privacy-gepruefte Wiki-Erinnerungen aus vault/Wiki.",
    }


def read_memory_wiki_page(path: str) -> dict[str, str]:
    vault_root = settings.vault_root.resolve()
    requested = (vault_root / path).resolve()
    wiki_root = (vault_root / "Wiki").resolve()
    if not requested.is_relative_to(wiki_root):
        raise ValueError("Only pages inside vault/Wiki can be read as long-term memory.")
    if requested.name in {"index.md", "log.md"} or requested.suffix != ".md":
        raise ValueError("Only concrete wiki memory pages can be read.")
    if not requested.is_file():
        raise FileNotFoundError(f"Memory wiki page does not exist: {path}")

    return {
        "path": requested.relative_to(vault_root).as_posix(),
        "markdown": requested.read_text(encoding="utf-8"),
    }


def get_memory_wiki_schema() -> dict[str, str]:
    return {"markdown": memory_schema_markdown()}


def lint_memory_wiki_pages() -> dict[str, Any]:
    return lint_memory_wiki(settings.vault_root)


def list_exported_documents() -> dict[str, Any]:
    export_root = settings.export_root
    suffix_labels = {
        ".docx": "docx",
        ".md": "markdown",
        ".pdf": "pdf",
        ".odt": "odt",
        ".zip": "package",
    }
    documents = []
    if export_root.is_dir():
        for path in sorted(export_root.rglob("*")):
            if not path.is_file() or path.name == ".gitkeep":
                continue
            documents.append(
                {
                    "filename": path.name,
                    "path": path.relative_to(export_root).as_posix(),
                    "type": suffix_labels.get(path.suffix.lower(), "file"),
                    "bytes": path.stat().st_size,
                }
            )

    return {
        "count": len(documents),
        "documents": documents,
        "root": export_root.as_posix(),
    }


def get_claude_os_memory_status() -> dict[str, Any]:
    return inspect_claude_os_runtime(
        settings.claude_os_url,
        project_name=settings.claude_os_project_name,
        wiki_kb_name=settings.claude_os_wiki_kb_name,
        wiki_mcp_type=settings.claude_os_wiki_mcp_type,
    )


def sync_claude_os_wiki_memory() -> dict[str, Any]:
    return sync_claude_os_memory(
        settings.claude_os_url,
        project_name=settings.claude_os_project_name,
        wiki_mcp_type=settings.claude_os_wiki_mcp_type,
    )


def search_claude_os_wiki_memory(
    query: str,
    use_hybrid: bool = False,
    use_rerank: bool = False,
    use_agentic: bool = False,
) -> dict[str, Any]:
    return search_claude_os_memory(
        settings.claude_os_url,
        wiki_kb_name=settings.claude_os_wiki_kb_name,
        query=query,
        use_hybrid=use_hybrid,
        use_rerank=use_rerank,
        use_agentic=use_agentic,
    )


def get_stack_status() -> dict[str, Any]:
    return build_stack_status(
        vault_root=settings.vault_root,
        export_root=settings.export_root,
        claude_os_url=settings.claude_os_url,
        claude_os_frontend_url=settings.claude_os_frontend_url,
        claude_os_redis_host=settings.claude_os_redis_host,
        claude_os_redis_port=settings.claude_os_redis_port,
        librechat_url=settings.librechat_url,
        ollama_url=settings.ollama_base_url,
        ollama_model=settings.ollama_model,
        ollama_embed_model=settings.ollama_embed_model,
        claude_os_project_name=settings.claude_os_project_name,
        claude_os_wiki_kb_name=settings.claude_os_wiki_kb_name,
        claude_os_wiki_mcp_type=settings.claude_os_wiki_mcp_type,
        public_host=settings.stack_public_host,
        host_librechat_port=settings.host_librechat_port,
        host_teacher_tools_port=settings.host_teacher_tools_port,
        host_claude_os_port=settings.host_claude_os_port,
        host_claude_os_frontend_port=settings.host_claude_os_frontend_port,
    )


def get_memory_wiki_index() -> str:
    _path, markdown = read_memory_index(settings.vault_root)
    return markdown


def get_curriculum_records() -> str:
    return json.dumps(_records(), ensure_ascii=False, indent=2)


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(
        "ai-teacher-stack teacher tools",
        host=settings.teacher_tools_mcp_host,
        port=settings.teacher_tools_mcp_port,
        stateless_http=True,
        json_response=True,
        instructions=(
            "Tools for privacy-conscious teacher planning. Do not request or store "
            "student names, grades, diagnoses, parent communication, health data, "
            "credentials, or confidential school documents. Long-term memory tools "
            "read only privacy-checked vault/Wiki pages and Claude-OS wiki KB state; "
            "cite local wiki paths or exported document paths when using them."
        ),
    )

    mcp.tool()(search_curriculum_records)
    mcp.tool()(create_lesson_markdown)
    mcp.tool()(export_lesson_docx_file)
    mcp.tool()(create_weekly_plan_markdown)
    mcp.tool()(create_memory_source_note)
    mcp.tool()(write_memory_wiki_page)
    mcp.tool()(promote_memory_source_note)
    mcp.tool()(list_memory_wiki_pages)
    mcp.tool()(read_memory_wiki_page)
    mcp.tool()(get_memory_wiki_schema)
    mcp.tool()(lint_memory_wiki_pages)
    mcp.tool()(list_exported_documents)
    mcp.tool()(get_claude_os_memory_status)
    mcp.tool()(sync_claude_os_wiki_memory)
    mcp.tool()(search_claude_os_wiki_memory)
    mcp.tool()(get_stack_status)
    mcp.resource("teacher://memory/wiki/index")(get_memory_wiki_index)
    mcp.resource("teacher://curriculum/records")(get_curriculum_records)
    return mcp


mcp = create_mcp_server()


def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
