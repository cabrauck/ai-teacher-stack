# Contributor Workflow Standard

This standard applies to contributor onboarding, issues, pull requests, specs,
agent instructions, and development documentation.

## Goals

- A contributor can clone the repository, connect any reasonable coding IDE or
  agent, run checks, and start work without private maintainer context.
- GitHub Project `ai-teacher-stack Roadmap` is the visible coordination board
  for open roadmap issues, spec shaping, implementation status, and PR review
  flow.
- The root `README.md` remains user-facing. Contributor workflow lives in
  `CONTRIBUTING.md`, `docs/`, `AGENTS.md`, `CLAUDE.md`, and Agent-OS.
- GitHub is the development workspace. GitHub Releases are user-only runtime
  packages.

## Contributor entrypoints

- `CONTRIBUTING.md` is the main contributor entrypoint.
- `docs/contributor-setup.md` provides IDE-agnostic setup.
- `AGENTS.md` and `CLAUDE.md` provide agent-specific operating context.
- Agent-OS product docs and standards provide decision context for larger work.

## Work paths

Direct fixes are acceptable for small bug fixes, focused documentation
improvements, and low-risk cleanup that preserves product, privacy, release, and
security boundaries.

Use Agent-OS for:

- new features
- cross-module changes
- release-boundary changes
- curriculum grounding changes
- export or vault structure changes
- privacy or security behavior changes

Agent-OS-scoped work must be implemented only from a spec marked `Ready` or
`In Progress`. A `Draft` spec must be shaped before runtime implementation.

## Roadmap governance

Contributors may propose roadmap changes through issues, specs, or pull
requests. The maintainer owns final roadmap direction, milestone priority, and
release timing.

Roadmap changes must explain the teacher workflow impact, affected privacy and
security boundaries, release-package implications, and required verification.

Open roadmap work should be represented as GitHub Issues and added to the
GitHub Project. Agent-OS remains the decision and specification layer for larger
changes; the GitHub Project tracks coordination and status.

## PR expectations

- Keep changes scoped to the task and relevant spec.
- Add tests for non-trivial behavior.
- Run the smallest relevant check set before requesting review.
- Keep contributor and Agent-OS material out of user release packages.
- Do not include real classroom material, credentials, local exports, vault
  notes, or Claude-OS runtime state.

## Documentation split

- User pitch and local usage: `README.md`
- Contributor workflow: `CONTRIBUTING.md` and `docs/contributor-setup.md`
- Runtime/user package policy: `docs/release-policy.md`
- Privacy boundary: `docs/privacy-boundary.md`
- Agent execution context: `AGENTS.md` and `CLAUDE.md`
- Feature decisions and tasks: `agent-os/`
