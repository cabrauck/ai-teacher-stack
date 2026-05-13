from pathlib import Path

from teacher_tools.curriculum import load_curriculum_records
from teacher_tools.documents import lesson_to_markdown
from teacher_tools.lessons import generate_lesson_plan
from teacher_tools.models import LessonRequest


def curriculum_root() -> Path:
    return Path(__file__).resolve().parents[4] / "data" / "curriculum"


def test_generate_lesson_plan():
    records = load_curriculum_records(curriculum_root())
    lesson = generate_lesson_plan(
        LessonRequest(subject="HSU", grade_band="3/4", topic="Orientierung mit Karten"),
        records,
    )
    assert lesson.title == "HSU: Orientierung mit Karten"
    assert lesson.curriculum_references


def test_lesson_to_markdown_contains_review_note():
    records = load_curriculum_records(curriculum_root())
    lesson = generate_lesson_plan(
        LessonRequest(subject="Deutsch", grade_band="3/4", topic="Lesen"),
        records,
    )
    markdown = lesson_to_markdown(lesson)
    assert "Automatisch erzeugter Entwurf" in markdown
    assert "# Deutsch: Lesen" in markdown
