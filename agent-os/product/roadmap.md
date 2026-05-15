# Roadmap

Agent-OS stays the repo-only developer/specification gate. LibreChat is the v1
teacher frontend. Claude-OS is the core runtime memory service. Obsidian is the
visible long-term memory surface.

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
- LibreChat is the selected v1 teacher frontend; alternative chat frontends are
  not tracked as product backlog.
- Open roadmap items are imported into GitHub Project `ai-teacher-stack
  Roadmap` as Issues.
- LehrplanPLUS ingestion is specified as `Ready`, but not implemented.
- Materiallizenzen and rights metadata are specified as `Draft`.
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
- Keep Claude-OS as the core memory service behind the LibreChat v1 frontend.

## v0.2.5 LibreChat v1 Frontend

- Add LibreChat as the default teacher frontend in Docker Compose.
- Use OpenRouter as the default model route with local BYOK options for selected
  frontier providers.
- Connect LibreChat tightly to Claude-OS and teacher-tools through MCP.
- Keep LibreChat RAG, vector DB, and search infrastructure out of the default
  stack when Claude-OS already provides the memory/knowledge path.
- Keep Claude Code, Codex App, and other coding-agent clients out of the product
  frontend backlog.

## v0.3 LehrplanPLUS Ingestion

- Define a controlled ingestion workflow for public LehrplanPLUS curriculum references.
- Store source URL and retrieval date with normalized records.
- Keep ingestion data separate from generated lesson content.
- Use the existing `lehrplanplus-ingestion` Agent-OS spec as the implementation gate.

## v0.4 Materiallizenzen and Rights Metadata

- Define metadata-first license handling for teacher-created material, OER,
  public curriculum references, publisher material, and unknown sources.
- Use `CC-BY-SA-4.0` as the planned default license option when teachers choose
  to share or publish self-created material.
- Keep publisher material as referenced metadata only unless explicit usage
  rights are documented by the teacher.
- Prepare contributor research work for German school copying rules, publisher
  license categories, and OER attribution models.
- Use the `material-lizenzen` Agent-OS spec as the shaping gate before runtime
  implementation.

## v0.5 DOCX Document Factory

- Expand DOCX export into a small document factory for lesson plans, worksheets,
  and solution keys.
- Add an OpenDocument Text (ODT) export path for LibreOffice-compatible workflows.
- Keep Markdown as the inspectable source or intermediate format.
- Use deterministic filenames and teacher-review notes.
- Render visible license metadata in Markdown and DOCX once the licensing model
  is implemented.

## v0.6 Optional Local AI/Ollama Support

- Add optional local AI workflows through Ollama after deterministic flows remain stable.
- Do not require Ollama for tests, bootstrap, or basic lesson export.
- Keep generated output curriculum-grounded and teacher-reviewed.

## Later: BYCS/OneDrive Export Adapters

- Consider explicit export adapters for BYCS or OneDrive.
- Keep adapters disabled by default and avoid autopublishing.
- Do not store credentials or school-internal confidential documents in the repository.

## Backlog Decisions

- Evaluate Open Design as a teacher-facing branding/material design tool for
  consistent worksheets, plans, board prompts, and export templates.
- Decide later whether Open Design also supports v2 development work around the
  Vercel AI SDK custom frontend.
- Add browser preview for DOCX/PDF/ODT after the LibreChat v1 workflow is
  stable.
- Build the v2 custom frontend with Vercel AI SDK after the teacher-tools,
  Claude-OS, MCP, and preview seams are stable.

## Out of Scope

- Student accounts, gradebooks, learner analytics, parent communication, behavior
  incident records, or central multi-user school platform features.
- Commercial textbook ingestion by default.
- Automated legal clearance for publisher materials or license terms.
- Claims of certified DSGVO, BSI IT-Grundschutz, or NIS2 compliance.
