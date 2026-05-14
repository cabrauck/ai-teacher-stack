from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from teacher_tools.curriculum import load_curriculum_records, search_curriculum
from teacher_tools.documents import (
    export_lesson_docx,
    export_schriftwesen_docx,
    lesson_to_markdown,
)
from teacher_tools.lessons import generate_lesson_plan
from teacher_tools.memory import (
    create_source_note,
    memory_health,
    promote_source_to_wiki,
    read_memory_index,
    write_wiki_page,
)
from teacher_tools.models import ExportRequest, LessonRequest
from teacher_tools.privacy import PrivacyError
from teacher_tools.schriftwesen import (
    DailyTop,
    DailyTopRequest,
    HandoverSummary,
    HandoverSummaryRequest,
    SubstitutionPlan,
    SubstitutionPlanRequest,
    WeeklyPlan,
    WeeklyPlanRequest,
    generate_daily_top,
    generate_handover_summary,
    generate_substitution_plan,
    generate_weekly_plan,
    schriftwesen_to_markdown,
)
from teacher_tools.settings import settings
from teacher_tools.stack_status import build_stack_status

app = FastAPI(title="ai-teacher-stack local teacher tools", version="0.1.0")

SchriftwesenDocumentPayload = Annotated[
    WeeklyPlan | DailyTop | SubstitutionPlan | HandoverSummary,
    Field(discriminator="typ"),
]


class SchriftwesenMarkdownRequest(BaseModel):
    document: SchriftwesenDocumentPayload


class SchriftwesenDocxRequest(BaseModel):
    document: SchriftwesenDocumentPayload
    filename: str | None = None


class MemorySourceRequest(BaseModel):
    title: str
    body: str
    source_type: str = "note"
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)


class MemoryWikiRequest(BaseModel):
    title: str
    body: str
    tags: list[str] = Field(default_factory=list)
    source_path: str | None = None
    metadata: dict[str, object] = Field(default_factory=dict)


class MemoryPromotionRequest(BaseModel):
    source_path: str
    title: str | None = None
    summary: str | None = None
    tags: list[str] = Field(default_factory=list)


def _memory_error(exc: Exception) -> HTTPException:
    if isinstance(exc, PrivacyError):
        return HTTPException(status_code=400, detail=str(exc))
    if isinstance(exc, FileNotFoundError):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    return HTTPException(status_code=500, detail=str(exc))


def _memory_write_response(result) -> dict[str, str]:
    return {
        "title": result.title,
        "slug": result.slug,
        "path": result.relative_path,
        "privacy_status": result.privacy_status,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/status")
def stack_status():
    return build_stack_status(
        vault_root=settings.vault_root,
        export_root=settings.export_root,
        claude_os_url=settings.claude_os_url,
    )


@app.get("/curriculum/search")
def curriculum_search(q: str = ""):
    records = load_curriculum_records(settings.curriculum_root)
    return {"query": q, "results": search_curriculum(records, q)}


@app.post("/lessons")
def lessons(request: LessonRequest):
    records = load_curriculum_records(settings.curriculum_root)
    lesson = generate_lesson_plan(request, records)
    return lesson


@app.post("/lessons/markdown")
def lesson_markdown(request: LessonRequest):
    records = load_curriculum_records(settings.curriculum_root)
    lesson = generate_lesson_plan(request, records)
    return {"markdown": lesson_to_markdown(lesson)}


@app.post("/exports/docx")
def export_docx(request: ExportRequest):
    path = export_lesson_docx(
        request.lesson,
        export_root=settings.export_root,
        filename=request.filename,
    )
    try:
        display_path = path.relative_to(Path("/app"))
    except ValueError:
        display_path = path
    return {"path": str(display_path)}


@app.post("/schriftwesen/weekly-plan")
def schriftwesen_weekly_plan(request: WeeklyPlanRequest):
    return generate_weekly_plan(request)


@app.post("/schriftwesen/daily-top")
def schriftwesen_daily_top(request: DailyTopRequest):
    return generate_daily_top(request)


@app.post("/schriftwesen/substitution-plan")
def schriftwesen_substitution_plan(request: SubstitutionPlanRequest):
    return generate_substitution_plan(request)


@app.post("/schriftwesen/handover-summary")
def schriftwesen_handover_summary(request: HandoverSummaryRequest):
    return generate_handover_summary(request)


@app.post("/schriftwesen/markdown")
def schriftwesen_markdown(request: SchriftwesenMarkdownRequest):
    return {"markdown": schriftwesen_to_markdown(request.document)}


@app.post("/schriftwesen/docx")
def schriftwesen_docx(request: SchriftwesenDocxRequest):
    path = export_schriftwesen_docx(
        request.document,
        export_root=settings.export_root,
        filename=request.filename,
    )
    try:
        display_path = path.relative_to(Path("/app"))
    except ValueError:
        display_path = path
    return {"path": str(display_path)}


@app.get("/memory/health")
def memory_status():
    return memory_health(settings.vault_root)


@app.post("/memory/sources")
def memory_source(request: MemorySourceRequest):
    try:
        result = create_source_note(
            settings.vault_root,
            title=request.title,
            body=request.body,
            source_type=request.source_type,
            tags=request.tags,
            metadata=request.metadata,
        )
    except Exception as exc:
        raise _memory_error(exc) from exc
    return _memory_write_response(result)


@app.post("/memory/wiki")
def memory_wiki(request: MemoryWikiRequest):
    try:
        result = write_wiki_page(
            settings.vault_root,
            title=request.title,
            body=request.body,
            tags=request.tags,
            source_path=request.source_path,
            metadata=request.metadata,
        )
    except Exception as exc:
        raise _memory_error(exc) from exc
    return _memory_write_response(result)


@app.get("/memory/wiki/index")
def memory_wiki_index():
    path, markdown = read_memory_index(settings.vault_root)
    try:
        display_path = path.relative_to(settings.vault_root)
    except ValueError:
        display_path = path
    return {"path": str(display_path), "markdown": markdown}


@app.post("/memory/wiki/promote")
def memory_promote(request: MemoryPromotionRequest):
    try:
        result = promote_source_to_wiki(
            settings.vault_root,
            source_path=request.source_path,
            title=request.title,
            summary=request.summary,
            tags=request.tags,
        )
    except Exception as exc:
        raise _memory_error(exc) from exc
    response = _memory_write_response(result.wiki)
    response["source_path"] = result.source_path
    return response
