# AGENTS.md

Instructions for Codex and other coding agents working in this repository.

## Mission

Build a local-first AI teacher stack for material planning, curriculum-grounded lesson design, Obsidian-based memory, and document export.

The stack should stay small and practical:

- Docker Compose, not a full homelab platform.
- Local files and Obsidian vault as the primary state.
- Teacher-only workflows in v1.
- No sensitive student data in default features.
- Curriculum grounding before generative output.
- DOCX and Markdown exports before UI complexity.

## Development commands

From repository root:

```bash
make check
make test
make lint
make up
make down
make release-check
```

From `services/teacher_tools`:

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv run uvicorn teacher_tools.api:app --reload --port 8010
```

## Coding conventions

- Keep domain logic in pure functions under `teacher_tools`.
- Keep FastAPI request and response models under `teacher_tools/api.py`.
- Keep document export isolated under `teacher_tools/documents.py`.
- Keep curriculum loading and search isolated under `teacher_tools/curriculum.py`.
- Add tests for every non-trivial behavior.
- Do not call external APIs in tests.
- Do not require Ollama for tests.

## Release and workspace policy

- Treat the GitHub repository as the development workspace.
- Treat GitHub Releases as user-only runtime packages.
- Do not create a dev release ZIP; developers should clone the repository.
- Keep Agent-OS, specs, tests, `.claude/`, `.github/`, `AGENTS.md`, and `CLAUDE.md` out of user release packages.
- Keep user releases limited to runtime files, sample curriculum data, prompts, templates, empty vault/export skeletons, and user documentation.
- When adding runtime files, update `scripts/build_release.py` and run `make release-check`.
- When adding dev tooling or specs, keep them repo-only and outside the release allowlist.

## Hard boundaries

Do not add features that require or encourage committing student names, grades, diagnoses, parent communication, credentials, BYCS or OneDrive tokens, or copyrighted textbook content.
