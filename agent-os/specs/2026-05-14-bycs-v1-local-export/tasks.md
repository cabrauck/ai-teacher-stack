# Tasks: ByCS v1 Local Export

Status: Done

## Implementation

- [x] Add `teacher_tools.bycs` package.
- [x] Add local export profile and space models.
- [x] Add privacy validation for obvious sensitive fields.
- [x] Add Drive package export with `manifest.json`.
- [x] Add Office target type mapping and explicit unsupported-generator errors.
- [x] Add Board package export with `tafelbild.md`, `assets/`, and manifest.
- [x] Add CLI commands for Drive export, Board export, and validation.
- [x] Add example profile config.
- [x] Add ByCS export skeleton folders.
- [x] Update release boundary script for `.gitkeep` export skeletons only.

## Verification

- [x] Add tests for folder creation, manifests, spaces, privacy validation,
  Office type mapping, and Board package structure.
- [x] Run `uv run ruff check .`.
- [x] Run `uv run pytest`.
- [x] Run `python scripts/build_release.py --version dev --check`.
