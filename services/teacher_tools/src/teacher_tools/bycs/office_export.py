from __future__ import annotations

from pathlib import Path

from teacher_tools.bycs.models import ByCSMaterialType, ByCSOfficeFormat


class OfficeGenerationUnavailable(NotImplementedError):
    """Raised when a modeled Office target has no implemented generator yet."""


EXTENSION_TO_OFFICE_FORMAT = {
    ".docx": ByCSOfficeFormat.DOCX,
    ".xlsx": ByCSOfficeFormat.XLSX,
    ".pptx": ByCSOfficeFormat.PPTX,
    ".pdf": ByCSOfficeFormat.PDF,
    ".md": ByCSOfficeFormat.MARKDOWN,
    ".markdown": ByCSOfficeFormat.MARKDOWN,
}

DOCUMENT_KIND_TO_OFFICE_FORMAT = {
    "lesson_plan": ByCSOfficeFormat.DOCX,
    "verlaufsplan": ByCSOfficeFormat.DOCX,
    "worksheet": ByCSOfficeFormat.DOCX,
    "arbeitsblatt": ByCSOfficeFormat.DOCX,
    "solution": ByCSOfficeFormat.DOCX,
    "loesung": ByCSOfficeFormat.DOCX,
    "parent_letter": ByCSOfficeFormat.DOCX,
    "elternbrief": ByCSOfficeFormat.DOCX,
    "planning_table": ByCSOfficeFormat.XLSX,
    "planungsliste": ByCSOfficeFormat.XLSX,
    "presentation": ByCSOfficeFormat.PPTX,
    "praesentation": ByCSOfficeFormat.PPTX,
    "final": ByCSOfficeFormat.PDF,
    "board_final": ByCSOfficeFormat.PDF,
}

MATERIAL_TYPE_TO_OFFICE_FORMAT = {
    ByCSMaterialType.LESSON_PLAN: ByCSOfficeFormat.DOCX,
    ByCSMaterialType.WORKSHEET: ByCSOfficeFormat.DOCX,
    ByCSMaterialType.SOLUTION: ByCSOfficeFormat.DOCX,
    ByCSMaterialType.SPREADSHEET: ByCSOfficeFormat.XLSX,
    ByCSMaterialType.PRESENTATION: ByCSOfficeFormat.PPTX,
    ByCSMaterialType.PDF: ByCSOfficeFormat.PDF,
    ByCSMaterialType.BOARD: ByCSOfficeFormat.PDF,
    ByCSMaterialType.MARKDOWN_SOURCE: ByCSOfficeFormat.MARKDOWN,
}


def office_format_for_extension(path: str | Path) -> ByCSOfficeFormat | None:
    return EXTENSION_TO_OFFICE_FORMAT.get(Path(path).suffix.casefold())


def office_format_for_document_kind(kind: str) -> ByCSOfficeFormat:
    key = kind.strip().casefold().replace("-", "_").replace(" ", "_")
    try:
        return DOCUMENT_KIND_TO_OFFICE_FORMAT[key]
    except KeyError as exc:
        raise ValueError(f"Unsupported ByCS Office document kind: {kind}") from exc


def office_format_for_material_type(material_type: ByCSMaterialType) -> ByCSOfficeFormat | None:
    return MATERIAL_TYPE_TO_OFFICE_FORMAT.get(material_type)


def ensure_office_compatible_file(path: str | Path) -> ByCSOfficeFormat:
    office_format = office_format_for_extension(path)
    if office_format is None:
        raise ValueError(f"File is not a modeled ByCS Office target format: {path}")
    return office_format


def generate_office_document(*_args: object, **_kwargs: object) -> Path:
    raise OfficeGenerationUnavailable(
        "TODO: connect this interface to concrete DOCX/XLSX/PPTX/PDF generators. "
        "ByCS v1 only models compatible target formats and copies existing files."
    )
