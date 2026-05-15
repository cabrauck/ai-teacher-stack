# Contributing to ai-teacher-stack

Thanks for contributing. This repository is the development workspace for
`ai-teacher-stack`: a local-first AI teacher stack for curriculum-grounded
planning, document export, Obsidian-based memory, and teacher-only workflows.

The root `README.md` is intentionally written as a user-facing pitch. This file
is the contributor entrypoint.

## Clone, connect IDE, run checks

The normal contributor path is:

```bash
git clone https://github.com/cabrauck/ai-teacher-stack.git
cd ai-teacher-stack
cp .env.example .env
cd services/teacher_tools
uv sync --extra dev
uv run ruff check .
uv run pytest
cd ../..
python scripts/build_release.py --version dev --check
```

After that, open the repository root in your preferred IDE or coding agent.
VS Code, JetBrains IDEs, Cursor, Codex, Claude Code, and terminal-only workflows
all use the same checkout and checks. See
`docs/contributor-setup.md` for IDE-specific notes.

## Before you start

Read these files first:

1. `README.md`
2. `AGENTS.md`
3. `CLAUDE.md`
4. `docs/contributor-setup.md`
5. `docs/privacy-boundary.md`
6. `docs/release-policy.md`

For larger or cross-cutting work, also read:

1. `agent-os/product/mission.md`
2. `agent-os/product/roadmap.md`
3. `agent-os/product/tech-stack.md`
4. `agent-os/standards/index.yml`
5. The matching spec under `agent-os/specs/`

## Project guardrails

- Keep the stack small and practical.
- Prefer local files, Docker Compose, and Obsidian-compatible Markdown.
- Keep Claude-OS as the runtime memory layer over privacy-checked wiki content.
- Ground lesson generation in curriculum data before freeform generation.
- Treat DOCX and Markdown export as first-class outputs.
- Keep teacher workflows in scope; do not turn this into a student-data system.
- Do not add or normalize storage of student names, grades, diagnoses, parent
  communication, tokens, or copyrighted textbook content.
- Treat German data protection expectations as mandatory project policy.
- Treat BSI and NIS2 as best-effort engineering alignment targets, not as
  certification claims.

## Choose the right workflow

Use a direct fix for:

- small bug fixes
- focused documentation improvements
- low-risk cleanup that preserves the current product boundaries

Use the Agent-OS workflow for:

- new features
- cross-module changes
- release-boundary changes
- changes affecting curriculum grounding, exports, vault structure, or privacy
  behavior

Implement Agent-OS-scoped work only from a spec marked `Ready` or
`In Progress`. If the matching spec is still `Draft`, finish shaping the spec
before writing runtime code.

## Roadmap governance

Contributors may propose roadmap changes through issues, Agent-OS specs, or
pull requests. Maintainer review decides final roadmap direction, milestone
priority, and release timing.

Use the GitHub Project `ai-teacher-stack Roadmap` as the visible coordination
board for open roadmap issues, spec shaping, implementation status, and review
flow. Agent-OS remains the decision and specification layer for larger changes.

Roadmap proposals should state the teacher workflow impact, affected privacy and
security boundaries, release-package implications, and required verification.

## Local setup

Prerequisites:

- Git
- Docker Desktop or Docker Engine with Docker Compose
- optional: Ollama for local AI models
- optional: GitHub CLI `gh` for repository bootstrap workflows

From the repository root:

```bash
cp .env.example .env
make check
make test
make lint
make up
make down
make release-check
```

Windows fallback when `make` is unavailable:

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

Runtime smoke checks:

```bash
curl http://localhost:8010/health
curl http://localhost:8051/health
curl http://localhost:8010/status
curl "http://localhost:8010/curriculum/search?q=lesen"
```

Claude-OS creates its local `ai-teacher-stack` project and the wiki knowledge
base hook under `vault/Wiki/` on startup. The first content sync only runs when
the configured local Ollama embedding model is available.

The current pre-release is LibreChat-first for teacher workflows:

- LibreChat at `http://localhost:3080` as the v1 teacher frontend
- Claude-OS at `http://localhost:8051` as memory runtime and admin UI
- teacher-tools MCP as the LibreChat tool bridge
- `http://localhost:8010/status` as aggregated readiness endpoint

Example lesson request after `docker compose up --build`:

```bash
curl -X POST http://localhost:8010/lessons \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "HSU",
    "grade_band": "3/4",
    "topic": "Orientierung mit Karten",
    "duration_minutes": 45
  }'
```

## Bootstrap a public repository

The repository includes a bootstrap script for creating a public GitHub
repository from the scaffold.

```bash
./scripts/bootstrap-github-public.sh cabrauck ai-teacher-stack
```

General pattern:

```bash
./scripts/bootstrap-github-public.sh <github-owner> <repo-name>
```

The script checks `git` and `gh`, initializes a Git repository when needed,
creates the first commit, and either creates the public GitHub repository or
connects an existing repository.

Manual fallback:

```bash
git init
git add .
git commit -m "Initial ai-teacher-stack scaffold"
gh repo create <github-owner>/<repo-name> --public --source=. --remote=origin --push
```

## Technical overview

```text
LibreChat teacher frontend
        |
        v
teacher-tools API/MCP + Claude-OS + Obsidian vault
        |
        +--> teacher-tools API
        |       - search_curriculum
        |       - map_topic_to_curriculum
        |       - generate_lesson_plan
        |       - memory source/wiki operations
        |       - export_lesson_docx
        |
        +--> Claude-OS core memory service
        |       - MCP/search/recall over vault/Wiki
        |       - automatic wiki KB bootstrap on container startup
        |       - local state under .claude-os
        |
        +--> optional qdrant profile
        |
        +--> optional Ollama endpoint
        |
        +--> exports/
                - DOCX
                - Markdown
                - PDF later
```

## Repository structure

```text
.
├── AGENTS.md
├── CLAUDE.md
├── docker-compose.yml
├── .env.example
├── .github/workflows/release.yml
├── Makefile
├── agent-os/
├── data/curriculum/bayern/grundschule/klasse_3_4/sample_curriculum.json
├── docs/
├── integrations/claude-os/
├── prompts/
├── services/teacher_tools/
├── templates/docx/
├── vault/
└── scripts/
```

## Code layout expectations

- Keep domain logic in `services/teacher_tools/src/teacher_tools/`.
- Keep FastAPI request and response models in
  `services/teacher_tools/src/teacher_tools/api.py`.
- Keep curriculum loading and search in `teacher_tools/curriculum.py`.
- Keep document export in `teacher_tools/documents.py`.
- Keep Schriftwesen logic in `teacher_tools/schriftwesen.py`.
- Keep privacy validation shared in `teacher_tools/privacy.py`.
- Do not duplicate privacy checks across features.

## Testing expectations

- Add tests for every non-trivial behavior.
- Do not call external APIs in tests.
- Do not require Ollama in tests.
- For Python changes, run `uv run ruff check .` and `uv run pytest`.
- If docs, runtime files, packaging paths, or release boundaries are touched,
  run `python scripts/build_release.py --version dev --check`.

## Release boundary

GitHub is the development workspace. GitHub Releases are user-only runtime
packages.

Keep these repo-only:

- `agent-os/`
- `.claude/`
- `.github/`
- `AGENTS.md`
- `CLAUDE.md`
- tests, specs, and development-only tooling

When adding runtime files, update `scripts/build_release.py`. Do not add
developer-only files to the release allowlist.

## Security and compliance

The project is designed to support compliance-conscious workflows under German
data protection expectations. It does not claim certified DSGVO, BSI
IT-Grundschutz, or NIS2 compliance.

Default behavior must avoid personal student data, credentials, confidential
school documents, parent communication, grades, diagnoses, health data,
behavior records, and performance records. Cloud exports and integrations must
remain explicit opt-in features.

Use secure defaults, dependency hygiene, least privilege, secret-free repository
contents, local-first storage, and auditable release boundaries. Document
security and incident concerns in specs or pull requests when they are relevant.

## Pull request checklist

Before opening or merging a PR, make sure:

1. The change stays within the product and privacy boundaries.
2. The right workflow was used: direct fix or Agent-OS.
3. Tests were added for non-trivial behavior.
4. Required checks were run locally.
5. User-facing and developer-facing docs stay separated.
6. Release packaging is still correct when relevant.

## Documentation split

- Keep `README.md` focused on users, the project pitch, and local usage.
- Put contributor workflow and development policy in `CONTRIBUTING.md` and
  `docs/contributor-setup.md`.
- Put agent-specific operating instructions in `AGENTS.md` and `CLAUDE.md`.

If a README change makes contributor onboarding less discoverable, add or update
the link to this file instead of moving development detail back into the pitch.
