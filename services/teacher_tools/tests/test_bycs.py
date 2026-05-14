from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from teacher_tools.bycs.board_export import export_board_package, parse_board_markdown
from teacher_tools.bycs.drive_export import export_drive_package
from teacher_tools.bycs.export_profile import DEFAULT_BYCS_EXPORT_PROFILE, load_export_profile
from teacher_tools.bycs.models import (
    ByCSBoardSections,
    ByCSLessonMetadata,
    ByCSMaterialFile,
    ByCSMaterialType,
)
from teacher_tools.bycs.office_export import (
    OfficeGenerationUnavailable,
    ensure_office_compatible_file,
    generate_office_document,
    office_format_for_document_kind,
)
from teacher_tools.bycs.privacy import ByCSPrivacyError, assert_export_privacy, validate_privacy
from teacher_tools.bycs.spaces import normalize_space_name


def test_drive_export_creates_folder_structure_and_manifest(tmp_path: Path):
    source = tmp_path / "lesson.docx"
    source.write_text("placeholder docx bytes for copy test", encoding="utf-8")
    profile = DEFAULT_BYCS_EXPORT_PROFILE.model_copy(update={"target_root": tmp_path / "bycs"})
    metadata = ByCSLessonMetadata(
        title="Kartenarbeit",
        subject="HSU",
        grade_band="3/4",
        class_name="Klasse 3a",
        date=date(2026, 5, 18),
        topic="Kartenarbeit",
        source_vault_path="vault/Unterricht/2026-05-18_HSU_Kartenarbeit.md",
    )
    material = ByCSMaterialFile(source_path=source, material_type=ByCSMaterialType.LESSON_PLAN)

    result = export_drive_package(profile, metadata, [material])

    assert result.package_dir == (
        tmp_path
        / "bycs"
        / "drive"
        / "2026-2027"
        / "Klasse_3a"
        / "HSU"
        / "2026-05-18_Kartenarbeit"
    )
    assert (result.package_dir / "01_Verlaufsplan.docx").exists()
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["title"] == "Kartenarbeit"
    assert manifest["subject"] == "HSU"
    assert manifest["grade_band"] == "3/4"
    assert manifest["class_name"] == "Klasse 3a"
    assert manifest["date"] == "2026-05-18"
    assert manifest["material_types"] == ["lesson_plan"]
    assert manifest["privacy_status"] == "no_personal_data_detected"
    assert manifest["source_vault_path"] == "vault/Unterricht/2026-05-18_HSU_Kartenarbeit.md"
    assert "01_Verlaufsplan.docx" in manifest["files"]


def test_space_name_normalization_is_bycs_folder_safe():
    assert normalize_space_name("Fachteam HSU/Mathe äöü ß") == "Fachteam_HSU_Mathe_aeoeue_ss"


def test_privacy_validation_blocks_obvious_personal_fields():
    result = validate_privacy({"student_name": "Testkind", "topic": "Kartenarbeit"})
    assert not result.ok
    assert result.blocked_fields == ("student_name",)

    assert validate_privacy({"grade_band": "3/4"}).ok

    with pytest.raises(ByCSPrivacyError):
        assert_export_privacy({"diagnosis": "nicht erfassen"})


def test_office_type_mapping_and_missing_generator_contract():
    assert ensure_office_compatible_file("Arbeitsblatt.docx").value == "docx"
    assert ensure_office_compatible_file("Planung.xlsx").value == "xlsx"
    assert ensure_office_compatible_file("Tafelbild.pdf").value == "pdf"
    assert office_format_for_document_kind("presentation").value == "pptx"

    with pytest.raises(ValueError):
        ensure_office_compatible_file("notizen.txt")

    with pytest.raises(OfficeGenerationUnavailable):
        generate_office_document()


def test_board_export_writes_markdown_assets_and_manifest(tmp_path: Path):
    asset = tmp_path / "bild.png"
    asset.write_bytes(b"png")
    profile = DEFAULT_BYCS_EXPORT_PROFILE.model_copy(update={"target_root": tmp_path / "bycs"})
    metadata = ByCSLessonMetadata(
        title="Kartenarbeit",
        subject="HSU",
        grade_band="3/4",
        date=date(2026, 5, 18),
        topic="Kartenarbeit",
    )
    sections = ByCSBoardSections(
        heading="Kartenarbeit",
        learning_goal="Ich kann eine Karte lesen.",
        entry="Kartenausschnitt betrachten.",
        assignment="Finde drei Orte und markiere den Weg.",
        consolidation="Ergebnisse gemeinsam sichern.",
        memory_note="Karten zeigen Orte von oben.",
        differentiation="Hilfekarte mit Symbolen nutzen.",
    )

    result = export_board_package(profile, metadata, sections, assets=[asset])

    assert (result.package_dir / "tafelbild.md").exists()
    assert (result.package_dir / "assets" / "bild_01.png").exists()
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["material_types"] == ["markdown_source", "asset"]
    assert manifest["files"] == ["tafelbild.md", "assets/bild_01.png"]


def test_parse_board_markdown_requires_board_sections(tmp_path: Path):
    board = tmp_path / "board.md"
    board.write_text(
        """# Kartenarbeit

## Lernziel
Ich kann eine Karte lesen.

## Einstieg
Kartenausschnitt betrachten.

## Arbeitsauftrag
Finde drei Orte.

## Sicherung
Ergebnisse sichern.

## Merksatz
Karten zeigen Orte von oben.
""",
        encoding="utf-8",
    )

    sections = parse_board_markdown(board)

    assert sections.heading == "Kartenarbeit"
    assert sections.assignment == "Finde drei Orte."


def test_load_example_profile_yaml(tmp_path: Path):
    profile_path = tmp_path / "profile.yml"
    profile_path.write_text(
        """profile_name: default-local-bycs
target_root: exports/bycs
school_year: "2026-2027"
school_context: "grundschule"
default_space: "Klasse_3a"
include_pdf: true
include_docx: true
include_markdown_source: false
anonymize_filenames: true
""",
        encoding="utf-8",
    )

    profile = load_export_profile(profile_path)

    assert profile.profile_name == "default-local-bycs"
    assert profile.include_markdown_source is False
