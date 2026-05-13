from pathlib import Path

from teacher_tools.curriculum import load_curriculum_records
from teacher_tools.documents import export_lesson_docx
from teacher_tools.lessons import generate_lesson_plan
from teacher_tools.models import LessonRequest


def curriculum_root() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "curriculum"


def test_export_lesson_docx(tmp_path):
    records = load_curriculum_records(curriculum_root())
    lesson = generate_lesson_plan(
        LessonRequest(subject="HSU", grade_band="3/4", topic="Orientierung mit Karten"),
        records,
    )
    out = export_lesson_docx(lesson, tmp_path, "lesson.docx")
    assert out.exists()
