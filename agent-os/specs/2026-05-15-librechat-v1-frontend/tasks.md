# Tasks: LibreChat v1 Teacher Frontend

Status: Done

## Implementation

- [x] Add LibreChat and LibreChat MongoDB to Docker Compose.
- [x] Keep LibreChat RAG API, PGVector, and MeiliSearch out of the default
  runtime in favor of Claude-OS memory/knowledge.
- [x] Add LibreChat config with OpenRouter, artifacts, teacher-tools MCP, and
  Claude-OS MCP.
- [x] Add teacher-tools MCP service.
- [x] Extend stack status and scripts for LibreChat.
- [x] Update user, contributor, product, and release docs.
- [x] Update release packaging.

## Verification

- [x] Add or update Compose tests.
- [x] Add or update status tests.
- [x] Add MCP behavior tests.
- [x] Run `uv run ruff check .`.
- [x] Run `uv run pytest`.
- [x] Run `python scripts/build_release.py --version dev --check`.
