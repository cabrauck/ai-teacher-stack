# Release policy

GitHub is the development workspace. GitHub Releases are user-facing runtime
packages only.

## User release contents

The release asset is named `ai-teacher-stack-user-vX.Y.Z.zip` and contains:

- Docker Compose runtime files.
- `.env.example`.
- `services/teacher_tools` runtime source, `pyproject.toml`, `uv.lock`, and
  Dockerfile.
- Sample curriculum data under `data/curriculum/`.
- Prompts, templates, empty vault skeleton folders, and `exports/.gitkeep`.
- User documentation, license, notice, and citation metadata.

The user package must start with:

```bash
cp .env.example .env
docker compose up --build
```

## Repo-only development contents

These paths are for repository development and must not be included in user
release packages:

- `agent-os/`
- `.claude/`
- `.github/`
- `AGENTS.md`
- `CLAUDE.md`
- tests and specs
- release/build scripts except runtime helper scripts explicitly allowlisted
- caches, virtual environments, generated exports, local `.env`, and local
  vault documents

Developers and agents should clone the repository directly instead of using a
separate dev release ZIP.

## Agent rule

When adding or moving files, update `scripts/build_release.py` if the change
affects runtime packaging. Keep dev tooling outside the allowlist unless it is
explicitly needed by a teacher running the released package.

Run the boundary check before release:

```bash
make release-check
```
