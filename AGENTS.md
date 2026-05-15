# AGENTS.md

Instructions for Codex and other coding agents working in this repository.

## Mission

Build a local-first AI teacher stack for material planning, curriculum-grounded lesson design, Obsidian-based memory, and document export.

The stack should stay small and practical:

- Docker Compose, not a full homelab platform.
- Local files and Obsidian vault as the primary state.
- Claude-OS is the core local long-term-memory runtime over privacy-checked
  Obsidian wiki content.
- LibreChat is the v1 teacher frontend.
- Claude Code, Codex, and other coding agents are contributor tools, not
  teacher product frontends or release targets.
- Teacher-only workflows in v1.
- No sensitive student data in default features.
- Curriculum grounding before generative output.
- DOCX and Markdown exports before UI complexity.
- Schriftwesen and handover are first-class v1 workflows, separate from reflection.

## Development commands

The repository is intended to be contributor-ready: clone it, create `.env`
from `.env.example`, attach any coding IDE or agent, and run the checks below.
Use `CONTRIBUTING.md` and `docs/contributor-setup.md` as the human contributor
entrypoints.

From repository root:

```bash
make check
make test
make lint
make up
make down
make release-check
```

If `make` is unavailable on Windows, run the same checks directly:

```bash
cd services/teacher_tools
uv run ruff check .
uv run pytest
cd ../..
python scripts/build_release.py --version dev --check
```

From `services/teacher_tools`:

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv run uvicorn teacher_tools.api:app --reload --port 8010
```

## Agent-OS workflow

Agent-OS is the developer specification layer for larger changes. It is not a
runtime feature and must stay out of user release packages.
Agent-OS is not the teacher frontend and not the runtime memory layer; LibreChat
fills the v1 teacher frontend role and Claude-OS fills the runtime memory role.

Use Agent-OS for new features, cross-module changes, release-boundary changes,
or anything that affects curriculum grounding, exports, vault structure, or
privacy behavior. Small bug fixes may be implemented directly if they preserve
the existing product constraints and include appropriate tests.

Before implementing Agent-OS-scoped work:

1. Read `agent-os/product/mission.md`, `agent-os/product/roadmap.md`, and
   `agent-os/product/tech-stack.md`.
2. Read `agent-os/standards/index.yml` and the standards relevant to the work,
   especially `contributor-workflow` and `security-compliance` for governance,
   onboarding, privacy, and security-sensitive changes.
3. Find the matching spec under `agent-os/specs/`.
4. Implement only from a spec with `Status: Ready` or `Status: In Progress`.
   If the matching spec is `Draft`, finish shaping it before implementation.
5. Update the spec/task status when implementation begins or finishes.

Spec status values:

- `Draft` - intent is captured, but decisions are incomplete.
- `Ready` - the work is decision-complete and can be implemented.
- `In Progress` - implementation has started.
- `Done` - implementation, tests, docs, and release-boundary checks are done.
- `Deferred` - intentionally postponed.

Definition of Done for Agent-OS-scoped work:

- Relevant standards are referenced or summarized in the spec.
- Acceptance criteria are concrete enough to test.
- Tests are named for non-trivial behavior.
- `uv run ruff check .` and `uv run pytest` pass for Python changes.
- `python scripts/build_release.py --version dev --check` passes when docs,
  runtime files, release files, or packaging boundaries are touched.
- Agent-OS, specs, tests, `.claude/`, `.github/`, `AGENTS.md`, and `CLAUDE.md`
  remain outside user release packages.
- Roadmap changes may be proposed by contributors, but maintainer review decides
  final roadmap direction, milestone priority, and release timing.
- GitHub Project `ai-teacher-stack Roadmap` is the visible coordination board
  for issues and PR flow. Agent-OS remains the decision and specification layer.

## Coding conventions

- Keep domain logic in pure functions under `teacher_tools`.
- Keep FastAPI request and response models under `teacher_tools/api.py`.
- Keep document export isolated under `teacher_tools/documents.py`.
- Keep curriculum loading and search isolated under `teacher_tools/curriculum.py`.
- Keep Schriftwesen generation and handover logic isolated under `teacher_tools/schriftwesen.py`.
- Keep privacy validation shared under `teacher_tools/privacy.py`; do not duplicate feature-specific validators.
- Add tests for every non-trivial behavior.
- Do not call external APIs in tests.
- Do not require Ollama for tests.

## Release and workspace policy

- Treat the GitHub repository as the development workspace.
- Treat GitHub Releases as user-only runtime packages.
- Do not create a dev release ZIP; developers should clone the repository.
- Keep contributor onboarding IDE-agnostic: VS Code, JetBrains IDEs, Cursor,
  Codex, Claude Code, and terminal workflows should all work from the same
  checkout and checks.
- Keep Agent-OS, specs, tests, `.claude/`, `.github/`, `AGENTS.md`, and `CLAUDE.md` out of user release packages.
- Keep user releases limited to runtime files, sample curriculum data, prompts, templates, empty vault/export skeletons, and user documentation.
- When adding runtime files, update `scripts/build_release.py` and run `make release-check`.
- When adding dev tooling or specs, keep them repo-only and outside the release allowlist.

## Hard boundaries

Do not add features that require or encourage committing student names, grades, diagnoses, parent communication, credentials, BYCS or OneDrive tokens, or copyrighted textbook content.

For Schriftwesen, do not add fields or examples for student observations, Leistungsaufschreibungen, illness data, parent communication with clear names, or sensitive individual cases.

The project is designed to support compliance-conscious workflows under German
data protection expectations. Do not claim certified DSGVO, BSI IT-Grundschutz,
or NIS2 compliance. Treat German data protection expectations as mandatory
project policy and BSI/NIS2 as best-effort engineering alignment targets.
