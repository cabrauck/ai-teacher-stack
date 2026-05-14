from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from teacher_tools.memory import (
    create_source_note,
    promote_source_to_wiki,
    read_memory_index,
    slugify,
    write_wiki_page,
)
from teacher_tools.privacy import PrivacyError


def test_slugify_is_deterministic_and_filesystem_safe():
    assert slugify("Kartenarbeit: Wege beschreiben") == "kartenarbeit-wege-beschreiben"
    assert slugify("Schriftwesen Übergabe") == "schriftwesen-uebergabe"


def test_create_source_note_uses_sources_folder_and_privacy_status(tmp_path: Path):
    result = create_source_note(
        tmp_path,
        title="Kartenarbeit",
        body="Kartenlegenden und Wegbeschreibungen fuer Klasse 3/4.",
        source_type="reflection",
        tags=["hsu"],
        created_at=date(2026, 5, 14),
    )

    assert result.relative_path == "Sources/2026-05-14_kartenarbeit.md"
    assert result.privacy_status == "no_personal_data_detected"
    assert result.path.read_text(encoding="utf-8").startswith("---\ntype: memory_source")


def test_write_wiki_page_updates_index_and_log(tmp_path: Path):
    result = write_wiki_page(
        tmp_path,
        title="Kartenarbeit",
        body="Bewaehrte Struktur fuer Kartenstunden.",
        tags=["hsu", "planung"],
        updated_at=datetime(2026, 5, 14, 10, 0, tzinfo=UTC),
    )
    index_path, index = read_memory_index(tmp_path)
    log = (tmp_path / "Wiki" / "log.md").read_text(encoding="utf-8")

    assert result.relative_path == "Wiki/kartenarbeit.md"
    assert index_path == tmp_path / "Wiki" / "index.md"
    assert "[[kartenarbeit|Kartenarbeit]]" in index
    assert "wiki_write" in log


def test_promote_source_to_wiki_blocks_personal_frontmatter(tmp_path: Path):
    source_dir = tmp_path / "Sources"
    source_dir.mkdir(parents=True)
    source = source_dir / "bad.md"
    source.write_text(
        "---\nstudent_name: Nicht Erfassen\n---\n# Bad\n\nKeine Promotion.",
        encoding="utf-8",
    )

    with pytest.raises(PrivacyError):
        promote_source_to_wiki(tmp_path, source_path="Sources/bad.md")


def test_write_wiki_page_blocks_personal_markdown_fields(tmp_path: Path):
    with pytest.raises(PrivacyError):
        write_wiki_page(
            tmp_path,
            title="Nicht speichern",
            body="student_name: Nicht Erfassen",
        )


def test_promote_source_to_wiki_creates_privacy_checked_wiki_page(tmp_path: Path):
    source = create_source_note(
        tmp_path,
        title="Wochenplan Routinen",
        body="Materialausgabe am Montag, Reflexion am Freitag.",
        created_at=date(2026, 5, 14),
    )

    promotion = promote_source_to_wiki(
        tmp_path,
        source_path=source.relative_path,
        summary="Wochenplan-Routine: Materialausgabe am Montag, Reflexion am Freitag.",
        tags=["schriftwesen"],
        promoted_at=datetime(2026, 5, 14, 12, 0, tzinfo=UTC),
    )

    assert promotion.source_path == "Sources/2026-05-14_wochenplan-routinen.md"
    assert promotion.wiki.relative_path == "Wiki/wochenplan-routinen.md"
    markdown = promotion.wiki.path.read_text(encoding="utf-8")
    assert "promoted_from: Sources/2026-05-14_wochenplan-routinen.md" in markdown
