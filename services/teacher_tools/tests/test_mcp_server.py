from __future__ import annotations

from pathlib import Path

import pytest

from teacher_tools import mcp_server
from teacher_tools.privacy import PrivacyError


def test_mcp_lesson_markdown_uses_curriculum_records(tmp_path: Path, monkeypatch):
    curriculum_root = tmp_path / "curriculum"
    curriculum_root.mkdir()
    (curriculum_root / "sample.json").write_text(
        """
        {
          "id": "lp-1",
          "jurisdiction": "BY",
          "school_type": "Grundschule",
          "grade_band": "3/4",
          "subject": "HSU",
          "learning_area": "Orientierung",
          "competency": "Karten zur Orientierung nutzen.",
          "content_examples": ["Karten", "Legenden"],
          "source": {"title": "Sample", "url": "https://example.test"}
        }
        """,
        encoding="utf-8",
    )
    monkeypatch.setattr(mcp_server.settings, "curriculum_root", curriculum_root)

    result = mcp_server.create_lesson_markdown(
        subject="HSU",
        topic="Karten",
        grade_band="3/4",
    )

    assert "# HSU: Karten" in result["markdown"]
    assert "Karten zur Orientierung nutzen." in result["markdown"]


def test_mcp_memory_write_is_privacy_gated(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(mcp_server.settings, "vault_root", tmp_path)

    with pytest.raises(PrivacyError):
        mcp_server.write_memory_wiki_page(
            title="Sensitive",
            body="grade: 1",
        )


def test_mcp_weekly_plan_markdown_is_anonymized():
    result = mcp_server.create_weekly_plan_markdown(
        woche="2026-KW21",
        klasse="Klasse 3a",
        themen=["Kartenarbeit"],
    )

    assert "personenbezogene_daten: false" in result["markdown"]
    assert "Kartenarbeit" in result["markdown"]


def test_mcp_lists_and_reads_memory_wiki_pages(tmp_path: Path, monkeypatch):
    wiki_root = tmp_path / "Wiki"
    wiki_root.mkdir(parents=True)
    (wiki_root / "index.md").write_text("# Index\n", encoding="utf-8")
    (wiki_root / "log.md").write_text("# Log\n", encoding="utf-8")
    (wiki_root / "kartenarbeit.md").write_text(
        "# Kartenarbeit Routinen\n\nPartnerarbeit mit Kartensymbolen.",
        encoding="utf-8",
    )
    monkeypatch.setattr(mcp_server.settings, "vault_root", tmp_path)

    pages = mcp_server.list_memory_wiki_pages()
    page = mcp_server.read_memory_wiki_page("Wiki/kartenarbeit.md")

    assert pages["count"] == 1
    assert pages["pages"][0]["title"] == "Kartenarbeit Routinen"
    assert pages["pages"][0]["path"] == "Wiki/kartenarbeit.md"
    assert "Partnerarbeit" in page["markdown"]


def test_mcp_blocks_memory_reads_outside_wiki(tmp_path: Path, monkeypatch):
    source_root = tmp_path / "Sources"
    source_root.mkdir(parents=True)
    (source_root / "raw.md").write_text("# Raw\n", encoding="utf-8")
    monkeypatch.setattr(mcp_server.settings, "vault_root", tmp_path)

    with pytest.raises(ValueError):
        mcp_server.read_memory_wiki_page("Sources/raw.md")


def test_mcp_lists_exported_documents(tmp_path: Path, monkeypatch):
    (tmp_path / "lesson.docx").write_bytes(b"docx")
    (tmp_path / "bycs" / "drive").mkdir(parents=True)
    (tmp_path / "bycs" / "drive" / "package.zip").write_bytes(b"zip")
    (tmp_path / ".gitkeep").write_text("", encoding="utf-8")
    monkeypatch.setattr(mcp_server.settings, "export_root", tmp_path)

    result = mcp_server.list_exported_documents()

    assert result["count"] == 2
    assert result["documents"][0]["filename"] == "package.zip"
    assert result["documents"][0]["type"] == "package"
    assert result["documents"][1]["filename"] == "lesson.docx"
    assert result["documents"][1]["type"] == "docx"
