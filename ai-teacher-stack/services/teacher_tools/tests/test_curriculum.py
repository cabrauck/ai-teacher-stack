from pathlib import Path

from teacher_tools.curriculum import load_curriculum_records, map_topic_to_curriculum, search_curriculum


def curriculum_root() -> Path:
    return Path(__file__).resolve().parents[4] / "data" / "curriculum"


def test_load_sample_curriculum():
    records = load_curriculum_records(curriculum_root())
    assert records


def test_search_curriculum_finds_lesen():
    records = load_curriculum_records(curriculum_root())
    results = search_curriculum(records, "Lesen")
    assert any(record.subject == "Deutsch" for record in results)


def test_map_topic_to_curriculum_prefers_subject():
    records = load_curriculum_records(curriculum_root())
    results = map_topic_to_curriculum(
        records,
        subject="HSU",
        grade_band="3/4",
        topic="Orientierung mit Karten",
    )
    assert results
    assert results[0].subject == "HSU"
