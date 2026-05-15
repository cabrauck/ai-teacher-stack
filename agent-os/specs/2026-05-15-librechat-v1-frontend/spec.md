# Spec: LibreChat v1 Teacher Frontend

Status: Done

## Purpose

Make LibreChat the single v1 teacher frontend while keeping Claude-OS as the
local memory runtime and teacher-tools as the curriculum, export, Schriftwesen,
and privacy boundary.

## Product Boundary

- LibreChat is the teacher-facing v1 UI.
- OpenRouter is the default model route.
- BYOK for selected frontier providers is configured only through local `.env`
  values or LibreChat user settings.
- Claude-OS remains the memory/knowledge runtime over privacy-checked
  `vault/Wiki/`.
- teacher-tools exposes deterministic APIs and MCP tools for curriculum,
  exports, Schriftwesen, and privacy-gated memory writes.
- Claude Code, Codex App, LobeChat, AnythingLLM, and Msty are not v1 or v2
  product frontends and are not tracked as product backlog.

## Runtime Shape

- Docker Compose starts LibreChat, LibreChat MongoDB, teacher-tools,
  teacher-tools MCP, Claude-OS, and Claude-OS Redis.
- MongoDB remains because LibreChat needs it for app state.
- LibreChat RAG API, PGVector, and MeiliSearch are not default services.
  Knowledge and memory go through Claude-OS and teacher-tools MCP instead of a
  second RAG stack.
- LibreChat exposes `http://localhost:3080`; teacher-tools stays on `8010`;
  Claude-OS stays on `8051`; teacher-tools MCP listens internally on `8020`.
- LibreChat config includes OpenRouter, artifact-capable model specs, the
  teacher-tools MCP server, and the Claude-OS MCP server.

## Acceptance Criteria

- The user release opens with LibreChat as the documented teacher frontend.
- Stack status reports LibreChat, teacher-tools, Claude-OS, vault, exports, and
  memory readiness.
- LibreChat can reach teacher-tools MCP and Claude-OS MCP without enabling
  duplicate RAG/vector/search services by default.
- Release packages include LibreChat config and empty local storage skeletons
  only, not databases, uploads, logs, secrets, specs, tests, or agent files.
- Product docs no longer position Claude Code, Codex App, or chat-frontend
  alternatives as teacher frontends.

## Backlog

- Evaluate Open Design as a teacher-facing branding/material design tool.
- Decide later whether Open Design also supports Vercel AI SDK v2 frontend
  development.
- Add browser preview for DOCX/PDF/ODT after the LibreChat v1 workflow is
  stable.
- Build the v2 custom frontend with Vercel AI SDK after the MCP and preview
  surfaces are stable.

## Test Plan

- `uv run ruff check .`
- `uv run pytest`
- `python scripts/build_release.py --version dev --check`
- Compose tests for LibreChat, LibreChat MongoDB, teacher-tools MCP, Claude-OS,
  and absence of default LibreChat RAG/vector/search services.
- MCP tests for curriculum search, lesson Markdown, DOCX export, Schriftwesen,
  stack status, and privacy-gated memory writes.
