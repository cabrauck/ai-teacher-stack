from pathlib import Path

from fastapi import FastAPI

from teacher_tools.curriculum import load_curriculum_records, search_curriculum
from teacher_tools.documents import export_lesson_docx, lesson_to_markdown
from teacher_tools.lessons import generate_lesson_plan
from teacher_tools.models import ExportRequest, LessonRequest
from teacher_tools.settings import settings

app = FastAPI(title="ai-teacher-stack local teacher tools", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


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
