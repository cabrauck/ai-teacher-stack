from __future__ import annotations

from pathlib import Path
from typing import Any

from teacher_tools.bycs.models import ByCSExportProfile


def find_workspace_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "services" / "teacher_tools").is_dir() and (parent / "exports").is_dir():
            return parent
    return Path.cwd()


def resolve_target_root(path: str | Path) -> Path:
    target = Path(path)
    if target.is_absolute():
        return target
    return find_workspace_root() / target


DEFAULT_BYCS_EXPORT_PROFILE = ByCSExportProfile(
    profile_name="default-local-bycs",
    target_root=resolve_target_root("exports/bycs"),
    school_year="2026-2027",
    school_context="grundschule",
    default_space="Klasse_3a",
    include_pdf=True,
    include_docx=True,
    include_markdown_source=False,
    anonymize_filenames=True,
)


def _parse_scalar(value: str) -> str | bool:
    cleaned = value.strip()
    if cleaned.startswith(('"', "'")) and cleaned.endswith(('"', "'")):
        return cleaned[1:-1]
    if cleaned.casefold() == "true":
        return True
    if cleaned.casefold() == "false":
        return False
    return cleaned


def load_simple_yaml(path: Path) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise ValueError(f"Unsupported profile line in {path}: {line}")
        key, raw_value = stripped.split(":", 1)
        values[key.strip()] = _parse_scalar(raw_value)
    return values


def load_export_profile(profile: str | Path | None = None) -> ByCSExportProfile:
    if profile is None:
        return DEFAULT_BYCS_EXPORT_PROFILE

    profile_text = str(profile)
    if profile_text in {"default", "default-local-bycs"}:
        return DEFAULT_BYCS_EXPORT_PROFILE

    path = Path(profile_text)
    if not path.is_file():
        raise FileNotFoundError(f"ByCS export profile not found: {profile_text}")

    loaded = ByCSExportProfile.model_validate(load_simple_yaml(path))
    return loaded.model_copy(update={"target_root": resolve_target_root(loaded.target_root)})


def with_profile_overrides(
    profile: ByCSExportProfile,
    *,
    target_root: Path | None = None,
    default_space: str | None = None,
) -> ByCSExportProfile:
    updates: dict[str, object] = {}
    if target_root is not None:
        updates["target_root"] = resolve_target_root(target_root)
    if default_space is not None:
        updates["default_space"] = default_space
    if not updates:
        return profile
    return profile.model_copy(update=updates)
