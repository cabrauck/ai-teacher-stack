# Contributor setup

This guide is for contributors who want to clone the repository, connect their
preferred coding IDE or agent, and start working without a private maintainer
setup.

## Fast start

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

If `make` is available, the equivalent repository-root check is:

```bash
make check
```

Start the local runtime only when you need to inspect the stack manually:

```bash
make up
```

Stop it with:

```bash
make down
```

## IDE and agent setup

The project is IDE-agnostic. Use the same repository checkout and checks from
any editor or coding agent.

Recommended local baseline:

- Git
- Docker Desktop or Docker Engine with Docker Compose
- Python 3.12
- `uv`
- Optional: `make`
- Optional: Ollama for local model experiments

Use these entrypoints:

- VS Code: open the repository root and use the integrated terminal for `uv`
  and `make` commands.
- JetBrains IDEs: open the repository root, set the Python interpreter from the
  `services/teacher_tools` environment, and run tests from that service folder.
- Cursor: open the repository root and keep agent edits scoped to the current
  task and relevant Agent-OS spec.
- Codex: start from `AGENTS.md`, `CONTRIBUTING.md`, and this guide.
- Claude Code: start from `CLAUDE.md`, `AGENTS.md`, and this guide.
- Generic terminal workflow: use the commands in the fast start section.

## What to read before changing code

Read these for every contribution:

1. `README.md`
2. `CONTRIBUTING.md`
3. `AGENTS.md`
4. `docs/privacy-boundary.md`
5. `docs/release-policy.md`

For larger changes, also read:

1. `agent-os/product/mission.md`
2. `agent-os/product/roadmap.md`
3. `agent-os/product/tech-stack.md`
4. `agent-os/standards/index.yml`
5. The matching spec under `agent-os/specs/`

## Choosing a work path

Use a direct fix for small bugs, focused documentation changes, or low-risk
cleanup that preserves existing privacy, release, and product boundaries.

Use Agent-OS for new features, cross-module changes, release-boundary changes,
or anything affecting curriculum grounding, exports, vault structure, privacy,
or security posture.

Agent-OS work must use a spec marked `Ready` or `In Progress`. If the matching
spec is `Draft`, shape the spec before runtime implementation.

## Roadmap contributions

Contributors may propose roadmap changes through issues, specs, or pull
requests. Maintainer review decides final roadmap direction, milestone order,
and release timing.

Use the public GitHub Project `ai-teacher-stack Roadmap` for visible tracking.
Open roadmap items should be represented as GitHub Issues and linked to the
project. Use Agent-OS specs for decision-complete implementation work.

Roadmap proposals should explain:

- what teacher workflow improves
- which privacy and security boundaries are affected
- whether the change belongs in runtime, docs, Agent-OS, or release packaging
- which tests or release-boundary checks prove the change

## Privacy and security baseline

The project is designed to support compliance-conscious workflows under German
data protection expectations. It does not claim certified DSGVO, BSI
IT-Grundschutz, or NIS2 compliance.

Default behavior must avoid personal student data, credentials, confidential
school documents, parent communication, grades, diagnoses, health data,
behavior records, and performance records.

BSI and NIS2 are treated as best-effort engineering alignment targets:

- local-first storage by default
- explicit opt-in for cloud exports
- secret-free repository contents
- dependency hygiene
- least-privilege configuration
- auditable release package boundaries
- documented security and incident concerns in PRs when relevant

## Before opening a PR

Run the smallest relevant check set:

- Docs-only or release-boundary-sensitive change:
  `python scripts/build_release.py --version dev --check`
- Python change:
  `cd services/teacher_tools && uv run ruff check . && uv run pytest`
- Runtime stack change:
  `make check` and a manual `make up` smoke test when Docker is available

Do not include local `.env`, real vault notes, generated exports, Claude-OS
runtime state, credentials, or private school material in a pull request.
