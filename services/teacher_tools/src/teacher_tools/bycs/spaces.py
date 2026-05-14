from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from teacher_tools.bycs.models import ByCSExportProfile, ByCSSpace, ByCSSpaceType

GERMAN_ASCII = str.maketrans(
    {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
    }
)


def normalize_folder_name(value: str) -> str:
    cleaned = value.strip().translate(GERMAN_ASCII)
    cleaned = unicodedata.normalize("NFKD", cleaned).encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^\w.\-]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_.-")
    return cleaned or "Unbenannt"


def normalize_space_name(space: ByCSSpace | str) -> str:
    if isinstance(space, ByCSSpace):
        return normalize_folder_name(space.name)
    return normalize_folder_name(space)


def default_space(profile: ByCSExportProfile, space_name: str | None = None) -> ByCSSpace:
    return ByCSSpace(
        name=space_name or profile.default_space,
        space_type=ByCSSpaceType.CLASS_SPACE,
        school_year=profile.school_year,
    )


def space_export_path(profile: ByCSExportProfile, space: ByCSSpace) -> Path:
    school_year = space.school_year or profile.school_year
    parts = [
        profile.target_root,
        "spaces",
        normalize_folder_name(school_year),
        space.space_type.value,
        normalize_space_name(space),
    ]
    if space.subject:
        parts.append(normalize_folder_name(space.subject))
    return Path(*parts)
