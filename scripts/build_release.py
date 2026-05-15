#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


PACKAGE_ROOT = "ai-teacher-stack"
DEFAULT_VERSION = "dev"
FORBIDDEN_PARTS = {
    ".claude",
    ".git",
    ".github",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "agent-os",
    "tests",
}
FORBIDDEN_NAMES = {"AGENTS.md", "CLAUDE.md"}
REQUIRED_PACKAGE_PATHS = {
    ".env.example",
    "COPYING.md",
    "NOTICE.md",
    "README.md",
    "docker-compose.yml",
    "docs/architecture.md",
    "docs/pre-release-guide.md",
    "docs/privacy-boundary.md",
    "scripts/check-pre-release.ps1",
    "scripts/check-pre-release.sh",
    "exports/.gitkeep",
    "exports/bycs/board/.gitkeep",
    "exports/bycs/drive/.gitkeep",
    "exports/bycs/office/.gitkeep",
    "exports/bycs/spaces/.gitkeep",
    ".claude-os/.gitkeep",
    ".claude-os/data/.gitkeep",
    ".claude-os/logs/.gitkeep",
    ".claude-os/redis/.gitkeep",
    ".claude-os/uploads/.gitkeep",
    ".librechat/.gitkeep",
    ".librechat/images/.gitkeep",
    ".librechat/logs/.gitkeep",
    ".librechat/mongodb/.gitkeep",
    ".librechat/uploads/.gitkeep",
    "integrations/claude-os/bootstrap_vault.py",
    "integrations/claude-os/Dockerfile",
    "integrations/claude-os/README.md",
    "integrations/claude-os/entrypoint.sh",
    "integrations/librechat/librechat.yaml",
    "prompts/lesson-planner.md",
    "scripts/start-pre-release.ps1",
    "scripts/start-pre-release.sh",
    "scripts/stop-pre-release.ps1",
    "scripts/stop-pre-release.sh",
    "services/teacher_tools/Dockerfile",
    "services/teacher_tools/pyproject.toml",
    "services/teacher_tools/src/teacher_tools/api.py",
    "services/teacher_tools/src/teacher_tools/stack_status.py",
    "services/teacher_tools/uv.lock",
    "templates/docx/default_lesson_template.md",
    "templates/schriftwesen/klassenuebergabe-anonym.template.md",
    "templates/schriftwesen/mobile-reserve-kurzinfo.template.md",
    "templates/schriftwesen/top-tagesorganisationsplan.template.md",
    "templates/schriftwesen/vertretungstag.template.md",
    "templates/schriftwesen/wochenplan.template.md",
    "vault/Lehrplan/.gitkeep",
    "vault/Materialien/.gitkeep",
    "vault/Policies/.gitkeep",
    "vault/Reflexion/.gitkeep",
    "vault/Schriftwesen/.gitkeep",
    "vault/Sources/.gitkeep",
    "vault/Templates/Schriftwesen/.gitkeep",
    "vault/Unterricht/.gitkeep",
    "vault/Wiki/.gitkeep",
}


@dataclass(frozen=True)
class PackageEntry:
    source: Path
    target: PurePosixPath


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the user-only ai-teacher-stack release package."
    )
    parser.add_argument(
        "--version",
        default=os.getenv("GITHUB_REF_NAME") or os.getenv("RELEASE_VERSION") or DEFAULT_VERSION,
        help="Release version used in the archive name, for example v0.1.0.",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Directory for generated release artifacts.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Build and validate the package boundary. Validation always runs.",
    )
    return parser.parse_args()


def safe_version(version: str) -> str:
    cleaned = version.strip() or DEFAULT_VERSION
    return cleaned.replace("/", "-").replace("\\", "-")


def should_skip(path: Path) -> bool:
    if any(part in FORBIDDEN_PARTS for part in path.parts):
        return True
    if path.name in FORBIDDEN_NAMES:
        return True
    return path.suffix == ".pyc"


def add_file(
    entries: list[PackageEntry],
    repo_root: Path,
    source_rel: str,
    target_rel: str | None = None,
) -> None:
    source = repo_root / source_rel
    if not source.is_file():
        raise FileNotFoundError(f"Required release file is missing: {source_rel}")
    target = PurePosixPath(target_rel or source_rel)
    entries.append(PackageEntry(source=source, target=target))


def add_tree(entries: list[PackageEntry], repo_root: Path, source_rel: str) -> None:
    source_root = repo_root / source_rel
    if not source_root.is_dir():
        raise FileNotFoundError(f"Required release directory is missing: {source_rel}")

    for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
        rel = source.relative_to(repo_root)
        if should_skip(rel):
            continue
        entries.append(PackageEntry(source=source, target=PurePosixPath(rel.as_posix())))


def add_skeleton_keep_files(
    entries: list[PackageEntry],
    repo_root: Path,
    source_rel: str,
) -> None:
    source_root = repo_root / source_rel
    if not source_root.is_dir():
        raise FileNotFoundError(f"Required skeleton directory is missing: {source_rel}")

    for source in sorted(source_root.rglob(".gitkeep")):
        rel = source.relative_to(repo_root)
        entries.append(PackageEntry(source=source, target=PurePosixPath(rel.as_posix())))


def collect_entries(repo_root: Path) -> list[PackageEntry]:
    entries: list[PackageEntry] = []

    add_file(entries, repo_root, "docs/user-quickstart.md", "README.md")
    for source in (
        ".env.example",
        "COPYING.md",
        "CITATION.cff",
        "NOTICE.md",
        "docker-compose.yml",
        "docs/architecture.md",
        "docs/pre-release-guide.md",
        "docs/privacy-boundary.md",
        "integrations/librechat/librechat.yaml",
        "scripts/check-pre-release.ps1",
        "scripts/check-pre-release.sh",
        "scripts/init-vault.sh",
        "scripts/start-pre-release.ps1",
        "scripts/start-pre-release.sh",
        "scripts/stop-pre-release.ps1",
        "scripts/stop-pre-release.sh",
        "services/teacher_tools/Dockerfile",
        "services/teacher_tools/pyproject.toml",
        "services/teacher_tools/uv.lock",
    ):
        add_file(entries, repo_root, source)

    for directory in (
        "data/curriculum",
        "integrations/claude-os",
        "prompts",
        "services/teacher_tools/src",
        "templates",
    ):
        add_tree(entries, repo_root, directory)

    add_skeleton_keep_files(entries, repo_root, ".claude-os")
    add_skeleton_keep_files(entries, repo_root, ".librechat")
    add_skeleton_keep_files(entries, repo_root, "exports")
    add_skeleton_keep_files(entries, repo_root, "vault")

    targets = [entry.target for entry in entries]
    duplicates = sorted({str(target) for target in targets if targets.count(target) > 1})
    if duplicates:
        raise ValueError(f"Duplicate release targets: {', '.join(duplicates)}")

    return sorted(entries, key=lambda entry: str(entry.target))


def write_zip(entries: list[PackageEntry], archive_path: Path) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if archive_path.exists():
        archive_path.unlink()

    with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in entries:
            package_name = PurePosixPath(PACKAGE_ROOT) / entry.target
            info = zipfile.ZipInfo(str(package_name))
            info.date_time = (2026, 1, 1, 0, 0, 0)
            mode = 0o755 if entry.target.suffix == ".sh" else 0o644
            info.external_attr = mode << 16
            archive.writestr(info, entry.source.read_bytes())


def validate_zip(archive_path: Path) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        members = sorted(name for name in archive.namelist() if not name.endswith("/"))

    expected_prefix = f"{PACKAGE_ROOT}/"
    errors: list[str] = []
    relative_members: set[str] = set()

    for member in members:
        if not member.startswith(expected_prefix):
            errors.append(f"Archive member is outside {PACKAGE_ROOT}/: {member}")
            continue

        relative = PurePosixPath(member.removeprefix(expected_prefix))
        relative_members.add(relative.as_posix())
        parts = set(relative.parts)

        forbidden_parts = sorted(parts & FORBIDDEN_PARTS)
        if forbidden_parts:
            errors.append(f"Forbidden path part in user package: {member}")

        if relative.name in FORBIDDEN_NAMES:
            errors.append(f"Forbidden agent/dev file in user package: {member}")

        if relative.as_posix() == ".env":
            errors.append("User package must not include .env")

        if relative.as_posix().startswith("data/rag/"):
            errors.append(f"User package must not include data/rag: {member}")

        if relative.as_posix().startswith("data/qdrant/"):
            errors.append(f"User package must not include data/qdrant: {member}")

        if relative.as_posix().startswith("exports/") and relative.name != ".gitkeep":
            errors.append(f"User package must include only .gitkeep skeletons under exports/: {member}")

        if relative.as_posix().startswith("vault/") and relative.name != ".gitkeep":
            errors.append(f"User package must include only vault skeleton files: {member}")

        if relative.as_posix().startswith(".claude-os/") and relative.name != ".gitkeep":
            errors.append(f"User package must include only Claude-OS skeleton files: {member}")

        if relative.as_posix().startswith(".librechat/") and relative.name != ".gitkeep":
            errors.append(f"User package must include only LibreChat skeleton files: {member}")

    missing = sorted(REQUIRED_PACKAGE_PATHS - relative_members)
    if missing:
        errors.append(f"Missing required user package files: {', '.join(missing)}")

    if errors:
        raise ValueError("\n".join(errors))


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    version = safe_version(args.version)
    archive_path = repo_root / args.output_dir / f"ai-teacher-stack-user-{version}.zip"

    try:
        entries = collect_entries(repo_root)
        write_zip(entries, archive_path)
        validate_zip(archive_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Release package failed: {exc}", file=sys.stderr)
        return 1

    try:
        display_path = archive_path.relative_to(repo_root)
    except ValueError:
        display_path = archive_path

    print(f"Built {display_path} with {len(entries)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
