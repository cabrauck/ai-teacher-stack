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
- Claude-OS Docker integration runtime files under `integrations/claude-os/`.
- Empty Claude-OS runtime state skeletons under `.claude-os/`.
- Runtime helper scripts explicitly allowlisted for user startup and checks.
- User documentation, license, notice, and citation metadata.

The user package must start with:

```bash
./scripts/start-pre-release.sh
```

## Repo-only development contents

These paths are for repository development and must not be included in user
release packages:

- `agent-os/`
- `.claude/`
- `.github/`
- `AGENTS.md`
- `CLAUDE.md`
- `CONTRIBUTING.md`
- `docs/contributor-setup.md`
- tests and specs
- release/build scripts except runtime helper scripts explicitly allowlisted
- caches, virtual environments, generated exports, local `.env`, and local
  vault documents
- Claude-OS databases, logs, Redis state, uploads, or indexed knowledge content

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

## GitHub release automation

Publishing a tag that starts with `v` triggers `.github/workflows/release.yml`.
The workflow builds `ai-teacher-stack-user-vX.Y.Z.zip`, validates the release
boundary, and uploads the ZIP to the matching GitHub Release.

Use pre-release tags for teacher-testable builds until the runtime package has
been install-tested end to end:

```bash
git tag v0.1.0-pre.1
git push origin v0.1.0-pre.1
```

Tags containing `-pre.`, `-alpha.`, `-beta.`, or `-rc.` are marked as GitHub
pre-releases. Do not publish GitHub Packages for v1; the ZIP asset is the
supported user distribution format.
