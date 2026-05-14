from __future__ import annotations

from datetime import UTC, datetime
from datetime import date as dt_date
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ByCSSpaceType(StrEnum):
    CLASS_SPACE = "class_space"
    TEACHER_TEAM_SPACE = "teacher_team_space"
    SUBJECT_TEAM_SPACE = "subject_team_space"
    SCHOOL_ADMIN_SPACE = "school_admin_space"
    SCHOOL_OFFICE_SPACE = "school_office_space"
    SCHOOL_AUTHORITY_SPACE = "school_authority_space"


class ByCSOfficeFormat(StrEnum):
    DOCX = "docx"
    XLSX = "xlsx"
    PPTX = "pptx"
    PDF = "pdf"
    MARKDOWN = "md"


class ByCSMaterialType(StrEnum):
    LESSON_PLAN = "lesson_plan"
    WORKSHEET = "worksheet"
    SOLUTION = "solution"
    BOARD = "board"
    PDF = "pdf"
    MARKDOWN_SOURCE = "markdown_source"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    ASSET = "asset"
    INTERNAL_REFLECTION = "internal_reflection"


class ByCSExportProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_name: str
    target_root: Path = Path("exports/bycs")
    school_year: str
    school_context: str = "grundschule"
    default_space: str
    include_pdf: bool = True
    include_docx: bool = True
    include_markdown_source: bool = False
    anonymize_filenames: bool = True

    @field_validator("profile_name", "school_year", "school_context", "default_space")
    @classmethod
    def require_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value must not be empty")
        return cleaned


class ByCSSpace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    space_type: ByCSSpaceType = ByCSSpaceType.CLASS_SPACE
    subject: str | None = None
    school_year: str | None = None

    @field_validator("name")
    @classmethod
    def require_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("space name must not be empty")
        return cleaned


class ByCSLessonMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    subject: str
    grade_band: str
    date: dt_date
    topic: str | None = None
    class_name: str | None = None
    intended_bycs_use: list[str] = Field(
        default_factory=lambda: [
            "ByCS Drive: manuelle Ablage oder Desktop-Sync",
            "ByCS Spaces: Ablage im passenden lokalen Zielordner",
        ]
    )
    source_vault_path: str | None = None

    @field_validator("title", "subject", "grade_band")
    @classmethod
    def require_metadata_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("metadata value must not be empty")
        return cleaned


class ByCSManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    subject: str
    grade_band: str
    class_name: str | None = None
    date: dt_date
    material_types: list[ByCSMaterialType] = Field(default_factory=list)
    exported_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    privacy_status: str = "no_personal_data_detected"
    intended_bycs_use: list[str] = Field(default_factory=list)
    source_vault_path: str | None = None
    files: list[str] = Field(default_factory=list)


class ByCSMaterialFile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_path: Path
    material_type: ByCSMaterialType
    target_name: str | None = None
    internal_only: bool = False


class ByCSBoardSections(BaseModel):
    model_config = ConfigDict(extra="forbid")

    heading: str
    learning_goal: str
    entry: str
    assignment: str
    consolidation: str
    memory_note: str
    differentiation: str | None = None

    @field_validator(
        "heading",
        "learning_goal",
        "entry",
        "assignment",
        "consolidation",
        "memory_note",
    )
    @classmethod
    def require_section_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("board section value must not be empty")
        return cleaned


class ByCSExportResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    package_dir: Path
    manifest_path: Path
    files: list[Path] = Field(default_factory=list)
