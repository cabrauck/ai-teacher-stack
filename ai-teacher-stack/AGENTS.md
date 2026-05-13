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
- DOCX/Markdown exports before UI complexity.

## Current stack

- Python 3.12
- FastAPI for local HTTP tool API
- Optional MCP wrapper planned around the same `teacher_tools` functions
- Qdrant for local vector index placeholder
- Optional Ollama endpoint
- python-docx for DOCX export
- pytest + ruff for checks

## Hard boundaries

Do not add features that require or encourage committing:

- student names
- grades
- diagnoses
- parent communication
- private credentials
- BYCS/OneDrive tokens
- copyrighted textbook content

If a task requires these, implement only generic placeholders and document the privacy boundary.

## Development commands

From repository root:

```bash
make check
make test
make lint
make up
make down
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
- Keep FastAPI request/response models under `teacher_tools/api.py`.
- Keep document export isolated under `teacher_tools/documents.py`.
- Keep curriculum loading/search isolated under `teacher_tools/curriculum.py`.
- Add tests for every non-trivial behavior.
- Prefer deterministic outputs in tests.
- Do not call external APIs in tests.
- Do not require Ollama for tests.

## Suggested first milestones

1. Replace sample curriculum with an official-source ingestion pipeline.
2. Add proper curriculum references and source URLs.
3. Implement DOCX export with sections and tables.
4. Add Obsidian note generation.
5. Add optional local embedding/indexing.
6. Add BYCS/OneDrive export adapters as disabled-by-default integrations.

## Review checklist

Before completing any task:

- `make check` passes.
- No secrets or real teaching material were added.
- Public repo remains safe.
- Any new external dependency is justified in `docs/architecture.md` or an ADR.
- Any generated teaching content includes a disclaimer that it must be reviewed by a teacher.
