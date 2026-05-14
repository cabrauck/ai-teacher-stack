from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from teacher_tools.bycs.models import (
    ByCSBoardSections,
    ByCSExportProfile,
    ByCSExportResult,
    ByCSLessonMetadata,
    ByCSManifest,
    ByCSMaterialType,
)
from teacher_tools.bycs.privacy import assert_export_privacy
from teacher_tools.bycs.spaces import normalize_folder_name

BOARD_HEADINGS = {
    "lernziel": "learning_goal",
    "einstieg": "entry",
    "arbeitsauftrag": "assignment",
    "sicherung": "consolidation",
    "merksatz": "memory_note",
    "differenzierung": "differentiation",
}


def render_board_markdown(sections: ByCSBoardSections) -> str:
    parts = [
        f"# {sections.heading}",
        "",
        "## Lernziel",
        sections.learning_goal,
        "",
        "## Einstieg",
        sections.entry,
        "",
        "## Arbeitsauftrag",
        sections.assignment,
        "",
        "## Sicherung",
        sections.consolidation,
        "",
        "## Merksatz",
        sections.memory_note,
    ]
    if sections.differentiation:
        parts.extend(["", "## Differenzierung", sections.differentiation])
    return "\n".join(parts).rstrip() + "\n"


def parse_board_markdown(path: Path) -> ByCSBoardSections:
    text = path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem

    values: dict[str, str] = {"heading": title}
    matches = list(re.finditer(r"^##\s+(.+)$", text, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        heading = match.group(1).strip().casefold()
        key = BOARD_HEADINGS.get(heading)
        if key is None:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        values[key] = text[start:end].strip()

    missing = [
        heading
        for heading, key in BOARD_HEADINGS.items()
        if key != "differentiation" and not values.get(key)
    ]
    if missing:
        needed = ", ".join(sorted(missing))
        raise ValueError(f"Board Markdown is missing required sections: {needed}")

    return ByCSBoardSections.model_validate(values)


def board_package_path(profile: ByCSExportProfile, metadata: ByCSLessonMetadata) -> Path:
    topic = metadata.topic or metadata.title
    folder = normalize_folder_name(f"{metadata.date.isoformat()}_{metadata.subject}_{topic}")
    return profile.target_root / "board" / folder


def _copy_assets(package_dir: Path, assets: list[Path]) -> list[Path]:
    copied: list[Path] = []
    if not assets:
        return copied

    asset_dir = package_dir / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    for index, asset in enumerate(assets, start=1):
        if not asset.is_file():
            raise FileNotFoundError(f"Board asset not found: {asset}")
        target = asset_dir / f"bild_{index:02d}{asset.suffix.casefold()}"
        shutil.copy2(asset, target)
        copied.append(target)
    return copied


def export_board_package(
    profile: ByCSExportProfile,
    metadata: ByCSLessonMetadata,
    sections: ByCSBoardSections,
    *,
    assets: list[Path] | None = None,
) -> ByCSExportResult:
    validation = assert_export_privacy(profile, metadata, sections)
    package_dir = board_package_path(profile, metadata)
    package_dir.mkdir(parents=True, exist_ok=True)

    markdown_path = package_dir / "tafelbild.md"
    markdown_path.write_text(render_board_markdown(sections), encoding="utf-8")
    copied_assets = _copy_assets(package_dir, assets or [])

    files = [markdown_path, *copied_assets]
    material_types = [ByCSMaterialType.MARKDOWN_SOURCE]
    if copied_assets:
        material_types.append(ByCSMaterialType.ASSET)

    manifest = ByCSManifest(
        title=metadata.title,
        subject=metadata.subject,
        grade_band=metadata.grade_band,
        class_name=metadata.class_name,
        date=metadata.date,
        material_types=material_types,
        privacy_status=validation.privacy_status,
        intended_bycs_use=[
            "ByCS Board: manuelle Nutzung als digitales Tafelbild",
            "ByCS Drive: Ablage des Board-Exportpakets",
        ],
        source_vault_path=metadata.source_vault_path,
        files=[path.relative_to(package_dir).as_posix() for path in files],
    )
    manifest_path = package_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return ByCSExportResult(package_dir=package_dir, manifest_path=manifest_path, files=files)
