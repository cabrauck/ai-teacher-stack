from __future__ import annotations

import argparse
import json
from datetime import date as dt_date
from pathlib import Path

from teacher_tools.bycs.board_export import export_board_package, parse_board_markdown
from teacher_tools.bycs.drive_export import export_drive_package, validate_export_package
from teacher_tools.bycs.export_profile import load_export_profile, with_profile_overrides
from teacher_tools.bycs.models import ByCSLessonMetadata, ByCSMaterialFile, ByCSMaterialType
from teacher_tools.bycs.office_export import office_format_for_extension


def _parse_date(value: str | None) -> dt_date:
    if value is None:
        return dt_date.today()
    return dt_date.fromisoformat(value)


def _metadata_from_args(args: argparse.Namespace) -> ByCSLessonMetadata:
    source = Path(args.input)
    title = args.title or source.stem.replace("_", " ")
    return ByCSLessonMetadata(
        title=title,
        subject=args.subject,
        grade_band=args.grade_band,
        date=_parse_date(args.date),
        topic=args.topic or title,
        class_name=args.class_name,
        source_vault_path=str(source),
    )


def _load_profile(args: argparse.Namespace):
    profile = load_export_profile(args.profile)
    target_root = Path(args.target_root) if args.target_root else None
    return with_profile_overrides(profile, target_root=target_root, default_space=args.space)


def _material_from_input(path: Path, include_markdown_source: bool) -> list[ByCSMaterialFile]:
    office_format = office_format_for_extension(path)
    if office_format is None:
        return []
    if office_format.value == "md" and not include_markdown_source:
        return []

    material_type = {
        "docx": ByCSMaterialType.LESSON_PLAN,
        "xlsx": ByCSMaterialType.SPREADSHEET,
        "pptx": ByCSMaterialType.PRESENTATION,
        "pdf": ByCSMaterialType.PDF,
        "md": ByCSMaterialType.MARKDOWN_SOURCE,
    }[office_format.value]
    return [ByCSMaterialFile(source_path=path, material_type=material_type)]


def export_drive(args: argparse.Namespace) -> int:
    profile = _load_profile(args)
    source = Path(args.input)
    metadata = _metadata_from_args(args)
    materials = _material_from_input(source, profile.include_markdown_source or args.include_source)
    result = export_drive_package(profile, metadata, materials)
    print(
        json.dumps(
            {"package_dir": str(result.package_dir), "manifest": str(result.manifest_path)}
        )
    )
    return 0


def export_board(args: argparse.Namespace) -> int:
    profile = _load_profile(args)
    source = Path(args.input)
    sections = parse_board_markdown(source)
    metadata = _metadata_from_args(args)
    if args.title is None or args.topic is None:
        metadata = metadata.model_copy(
            update={
                "title": metadata.title if args.title else sections.heading,
                "topic": metadata.topic if args.topic else sections.heading,
            }
        )
    assets = [Path(asset) for asset in args.asset]
    result = export_board_package(profile, metadata, sections, assets=assets)
    print(
        json.dumps(
            {"package_dir": str(result.package_dir), "manifest": str(result.manifest_path)}
        )
    )
    return 0


def validate_export(args: argparse.Namespace) -> int:
    result = validate_export_package(Path(args.path))
    print(
        json.dumps(
            {
                "ok": result.ok,
                "privacy_status": result.privacy_status,
                "blocked_fields": list(result.blocked_fields),
                "warnings": list(result.warnings),
            }
        )
    )
    return 0 if result.ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create local ByCS-compatible export packages.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(command: argparse.ArgumentParser) -> None:
        command.add_argument(
            "--input",
            required=True,
            help="Local Markdown or Office-compatible file.",
        )
        command.add_argument(
            "--profile",
            default="default",
            help="Profile name or simple YAML file.",
        )
        command.add_argument("--target-root", help="Override profile target_root.")
        command.add_argument("--space", help="Override profile default_space.")
        command.add_argument("--title")
        command.add_argument("--topic")
        command.add_argument("--subject", required=True)
        command.add_argument("--grade-band", default="3/4")
        command.add_argument("--class-name")
        command.add_argument("--date", help="Lesson date as YYYY-MM-DD. Defaults to today.")

    drive = subparsers.add_parser("export-drive", help="Create a local ByCS Drive package.")
    add_common(drive)
    drive.add_argument(
        "--include-source",
        action="store_true",
        help="Copy Markdown source even when the profile disables source export.",
    )
    drive.set_defaults(func=export_drive)

    board = subparsers.add_parser("export-board", help="Create a local ByCS Board package.")
    add_common(board)
    board.add_argument("--asset", action="append", default=[], help="PNG/SVG/PDF asset to copy.")
    board.set_defaults(func=export_board)

    validate = subparsers.add_parser(
        "validate-export",
        help="Validate a ByCS export manifest/package.",
    )
    validate.add_argument("path")
    validate.set_defaults(func=validate_export)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
