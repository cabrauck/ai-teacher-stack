from __future__ import annotations

import json
from pathlib import Path

from teacher_tools.models import CurriculumRecord


def load_curriculum_records(root: Path) -> list[CurriculumRecord]:
    """Load all curriculum JSON files below root.

    The function expects files containing either a list of records or a single record.
    Invalid files should fail loudly during development.
    """
    records: list[CurriculumRecord] = []
    if not root.exists():
        return records

    for path in sorted(root.rglob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        items = raw if isinstance(raw, list) else [raw]
        records.extend(CurriculumRecord.model_validate(item) for item in items)

    return records


def search_curriculum(records: list[CurriculumRecord], query: str) -> list[CurriculumRecord]:
    """Simple deterministic keyword search over curriculum records."""
    q = query.casefold().strip()
    if not q:
        return records

    def haystack(record: CurriculumRecord) -> str:
        return " ".join(
            [
                record.subject,
                record.learning_area,
                record.competency,
                " ".join(record.content_examples),
            ]
        ).casefold()

    return [record for record in records if q in haystack(record)]


def map_topic_to_curriculum(
    records: list[CurriculumRecord],
    *,
    subject: str,
    grade_band: str,
    topic: str,
    limit: int = 5,
) -> list[CurriculumRecord]:
    """Map a teaching topic to relevant curriculum records with a transparent score."""
    topic_terms = {term.casefold() for term in topic.replace("/", " ").split() if len(term) > 2}
    subject_cf = subject.casefold().strip()
    grade_cf = grade_band.casefold().strip()

    scored: list[tuple[int, CurriculumRecord]] = []
    for record in records:
        score = 0
        if record.subject.casefold() == subject_cf:
            score += 5
        if record.grade_band.casefold() == grade_cf:
            score += 3

        text = " ".join(
            [
                record.learning_area,
                record.competency,
                " ".join(record.content_examples),
            ]
        ).casefold()

        score += sum(1 for term in topic_terms if term in text)

        if score > 0:
            scored.append((score, record))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [record for _, record in scored[:limit]]
