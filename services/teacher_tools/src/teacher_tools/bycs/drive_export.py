from __future__ import annotations

import json
import shutil
from pathlib import Path

from teacher_tools.bycs.models import (
    ByCSExportProfile,
    ByCSExportResult,
    ByCSLessonMetadata,
    ByCSManifest,
    ByCSMaterialFile,
    ByCSMaterialType,
    ByCSSpace,
)
from teacher_tools.bycs.privacy import (
    PrivacyValidationResult,
    assert_export_privacy,
    validate_privacy,
)
from teacher_tools.bycs.spaces import default_space, normalize_folder_name, normalize_space_name

DEFAULT_MATERIAL_LABELS = {
    ByCSMaterialType.LESSON_PLAN: "Verlaufsplan",
    ByCSMaterialType.WORKSHEET: "Arbeitsblatt",
    ByCSMaterialType.SOLUTION: "Loesung",
    ByCSMaterialType.BOARD: "Tafelbild",
    ByCSMaterialType.PDF: "Fassung",
    ByCSMaterialType.MARKDOWN_SOURCE: "Quelle_intern",
    ByCSMaterialType.SPREADSHEET: "Planung",
    ByCSMaterialType.PRESENTATION: "Praesentation",
    ByCSMaterialType.ASSET: "Material",
    ByCSMaterialType.INTERNAL_REFLECTION: "Reflexion_intern",
}


def drive_package_path(
    profile: ByCSExportProfile,
    metadata: ByCSLessonMetadata,
    space: ByCSSpace | None = None,
) -> Path:
    selected_space = space or default_space(profile, metadata.class_name or profile.default_space)
    topic = metadata.topic or metadata.title
    lesson_folder = normalize_folder_name(f"{metadata.date.isoformat()}_{topic}")
    return (
        profile.target_root
        / "drive"
        / normalize_folder_name(profile.school_year)
        / normalize_space_name(selected_space)
        / normalize_folder_name(metadata.subject)
        / lesson_folder
    )


def _target_filename(index: int, material: ByCSMaterialFile) -> str:
    source_suffix = material.source_path.suffix
    if material.target_name:
        target = Path(material.target_name)
        stem = normalize_folder_name(target.stem)
        suffix = target.suffix or source_suffix
        return f"{stem}{suffix}"

    label = DEFAULT_MATERIAL_LABELS[material.material_type]
    return f"{index:02d}_{label}{source_suffix}"


def _copy_materials(
    package_dir: Path,
    materials: list[ByCSMaterialFile],
    *,
    include_internal_reflections: bool,
) -> tuple[list[Path], list[ByCSMaterialType]]:
    copied: list[Path] = []
    material_types: list[ByCSMaterialType] = []
    visible_index = 1

    for material in materials:
        if (
            material.internal_only
            or material.material_type == ByCSMaterialType.INTERNAL_REFLECTION
        ) and not include_internal_reflections:
            continue

        if not material.source_path.is_file():
            raise FileNotFoundError(f"Material file not found: {material.source_path}")

        target = package_dir / _target_filename(visible_index, material)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(material.source_path, target)
        copied.append(target)
        material_types.append(material.material_type)
        visible_index += 1

    return copied, material_types


def write_manifest(package_dir: Path, manifest: ByCSManifest) -> Path:
    path = package_dir / "manifest.json"
    path.write_text(
        json.dumps(manifest.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def export_drive_package(
    profile: ByCSExportProfile,
    metadata: ByCSLessonMetadata,
    materials: list[ByCSMaterialFile] | None = None,
    *,
    space: ByCSSpace | None = None,
    include_internal_reflections: bool = False,
) -> ByCSExportResult:
    materials = materials or []
    validation = assert_export_privacy(profile, metadata, [item.model_dump() for item in materials])
    package_dir = drive_package_path(profile, metadata, space)
    package_dir.mkdir(parents=True, exist_ok=True)

    copied, material_types = _copy_materials(
        package_dir,
        materials,
        include_internal_reflections=include_internal_reflections,
    )
    manifest = ByCSManifest(
        title=metadata.title,
        subject=metadata.subject,
        grade_band=metadata.grade_band,
        class_name=metadata.class_name,
        date=metadata.date,
        material_types=material_types,
        privacy_status=validation.privacy_status,
        intended_bycs_use=metadata.intended_bycs_use,
        source_vault_path=metadata.source_vault_path,
        files=[path.name for path in copied],
    )
    manifest_path = write_manifest(package_dir, manifest)
    return ByCSExportResult(package_dir=package_dir, manifest_path=manifest_path, files=copied)


def validate_export_package(path: Path) -> PrivacyValidationResult:
    manifest_path = path if path.is_file() else path / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"ByCS export manifest not found: {manifest_path}")

    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    return validate_privacy(raw)
