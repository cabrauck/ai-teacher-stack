# Codex setup

Use Codex as a coding agent for this repository.

Useful first prompt:

```text
Read AGENTS.md, README.md, and docs/roadmap.md. Run the checks and propose the smallest next implementation step.
```

Agent-OS first prompt for larger features:

```text
Read AGENTS.md, agent-os/product/mission.md, agent-os/product/roadmap.md,
agent-os/product/tech-stack.md, and agent-os/standards/index.yml. Find the
matching spec under agent-os/specs/. If it is Ready, implement the next unchecked
task. If it is Draft, finish shaping the spec before writing runtime code.
```

Useful commands:

```bash
make check
make test
make lint
make release-check
make up
make down
```

Windows fallback when `make` is not installed:

```bash
cd services/teacher_tools
uv run ruff check .
uv run pytest
cd ../..
python scripts/build_release.py --version dev --check
```

## Agent-OS workflow

Agent-OS is repo-only planning and implementation control. It must not become a
teacher-facing runtime feature and must not be added to user release packages.

Use Agent-OS for larger features and cross-cutting changes:

1. Read product context in `agent-os/product/`.
2. Read relevant standards from `agent-os/standards/`.
3. Work from a spec in `agent-os/specs/`.
4. Implement only when the spec status is `Ready` or `In Progress`.
5. Move the spec to `In Progress` when implementation starts and `Done` only
   after tests, docs, and release-boundary checks pass.

Status model:

- `Draft` - still being shaped.
- `Ready` - decision-complete and implementable.
- `In Progress` - implementation has started.
- `Done` - implementation and verification are complete.
- `Deferred` - intentionally postponed.

Definition of Done:

- The spec names applicable standards and concrete acceptance criteria.
- Non-trivial behavior has tests.
- Python changes pass `uv run ruff check .` and `uv run pytest`.
- Packaging-sensitive changes pass
  `python scripts/build_release.py --version dev --check`.
- Agent-OS files, specs, `.claude/`, `.github/`, `AGENTS.md`, and `CLAUDE.md`
  remain repo-only.

Release packaging rules are documented in `docs/release-policy.md`. Agent and
spec tooling stays repo-only and must not be added to user release packages.
