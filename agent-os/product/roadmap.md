# Roadmap

Agent-OS stays the repo-only developer/specification gate. Claude-OS is the core
runtime memory service. Obsidian is the visible long-term memory surface.

The repository should remain contributor-ready: a contributor can clone it,
connect a coding IDE or agent, create `.env`, run checks, and start from public
repo context. Contributors may propose roadmap changes through issues, specs,
or pull requests. Maintainer review owns final roadmap direction, milestone
priority, and release timing.

GitHub Project `ai-teacher-stack Roadmap` is the visible coordination board for
open roadmap items, Agent-OS spec shaping, implementation status, and review
flow. Open roadmap work should be represented as GitHub Issues in that project.
Agent-OS remains the decision and specification layer for larger changes.

## Current Implementation State

- Scaffold, Docker Compose, FastAPI, sample curriculum search, Markdown lesson
  output, basic DOCX export, tests, and release boundary checks are in place.
- ByCS local export is implemented as a low-integration local packaging flow.
- Schriftwesen and handover are implemented, tested, and privacy-gated.
- Contributor onboarding and repo policy are maintained through
  `CONTRIBUTING.md`, `docs/contributor-setup.md`, and Agent-OS standards.
- Open roadmap items are imported into GitHub Project `ai-teacher-stack
  Roadmap` as Issues.
- LehrplanPLUS ingestion is specified as `Ready`, but not implemented.
- DOCX document factory is still `Draft`.

## v0.2 Obsidian LTM and Claude-OS Core Runtime

- Make `docker compose up` start `teacher-tools`, `claude-os`, and
  `claude-os-redis` by default on macOS and Windows through Docker Desktop/WSL2.
- Use Obsidian-compatible Markdown as the teacher-visible long-term memory.
- Store curated raw notes under `vault/Sources/`.
- Store privacy-checked synthesized memory under `vault/Wiki/`.
- Keep `vault/Wiki/index.md` and `vault/Wiki/log.md` as navigation and audit files.
- Treat Claude-OS as the local memory engine over `vault/Wiki/`, not as an
  optional later bridge.
- Keep teacher frontends interchangeable: Claude Code, Codex, chat LLM, or later UI.

## v0.3 LehrplanPLUS Ingestion

- Define a controlled ingestion workflow for public LehrplanPLUS curriculum references.
- Store source URL and retrieval date with normalized records.
- Keep ingestion data separate from generated lesson content.
- Use the existing `lehrplanplus-ingestion` Agent-OS spec as the implementation gate.

## v0.4 DOCX Document Factory

- Expand DOCX export into a small document factory for lesson plans, worksheets,
  and solution keys.
- Add an OpenDocument Text (ODT) export path for LibreOffice-compatible workflows.
- Keep Markdown as the inspectable source or intermediate format.
- Use deterministic filenames and teacher-review notes.

## v0.5 Optional Local AI/Ollama Support

- Add optional local AI workflows through Ollama after deterministic flows remain stable.
- Do not require Ollama for tests, bootstrap, or basic lesson export.
- Keep generated output curriculum-grounded and teacher-reviewed.

## Later: BYCS/OneDrive Export Adapters

- Consider explicit export adapters for BYCS or OneDrive.
- Keep adapters disabled by default and avoid autopublishing.
- Do not store credentials or school-internal confidential documents in the repository.

## Out of Scope

- Student accounts, gradebooks, learner analytics, parent communication, behavior
  incident records, or central multi-user school platform features.
- Commercial textbook ingestion by default.
- Claims of certified DSGVO, BSI IT-Grundschutz, or NIS2 compliance.
