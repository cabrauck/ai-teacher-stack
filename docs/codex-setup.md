# Codex setup

Use Codex as a coding agent for this repository.

Useful first prompt:

```text
Read AGENTS.md, README.md, and docs/roadmap.md. Run the checks and propose the smallest next implementation step.
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

Release packaging rules are documented in `docs/release-policy.md`. Agent and
spec tooling stays repo-only and must not be added to user release packages.
