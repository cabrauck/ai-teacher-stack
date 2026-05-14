# Requirements: Obsidian LTM and Claude-OS Core Runtime

Status: Ready

## Purpose

Define the local long-term-memory workflow that combines Obsidian-compatible
Markdown with Claude-OS as the core runtime memory service.

## Requirements

- Default Compose starts Claude-OS and Redis with `teacher-tools`.
- Claude-OS is pinned to a known upstream commit and built through Docker.
- Claude-OS startup automatically bootstraps a local wiki knowledge base for
  `vault/Wiki/` and skips raw `vault/Sources/` content.
- Windows and macOS use the same Compose path; Windows uses Docker Desktop with WSL2.
- `vault/Sources/` stores curated raw notes.
- `vault/Wiki/` stores only privacy-checked synthesized memory.
- `vault/Wiki/index.md` and `vault/Wiki/log.md` are maintained by runtime helpers.
- `teacher_tools.memory` exposes pure functions for source, wiki, index, log, and promotion behavior.
- FastAPI exposes frontend-agnostic `/memory/...` endpoints.
- Release packages include only runtime files and empty skeletons for memory state.

## Non-goals

- Do not vendor Claude-OS source.
- Do not require native Claude-OS installation.
- Do not require Ollama, Qdrant, or cloud services for tests.
- Do not store student records or sensitive individual cases.
