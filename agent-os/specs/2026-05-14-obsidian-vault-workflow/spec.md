# Spec: Obsidian LTM and Claude-OS Core Runtime

Status: Done

## Purpose

Implement Obsidian-compatible long-term memory as the visible teacher memory
surface and make Claude-OS the core local runtime memory service behind it.

## Product Boundary

- Agent-OS remains the first development gate for larger changes.
- Agent-OS is not a teacher frontend and not the runtime memory layer.
- Claude-OS is the core runtime memory service.
- Teacher frontends stay interchangeable: Claude Code, Codex, a chat LLM, or a later UI.

## Runtime Shape

- Default `docker compose up` starts `teacher-tools`, `claude-os`, and
  `claude-os-redis`.
- Claude-OS is built from `brobertsaz/claude-os` pinned to commit
  `ee7b62bc5bf36541018a1c14592bcac2b59022f9`.
- Windows support is through Docker Desktop with WSL2.
- macOS support is through Docker Desktop.
- Native Claude-OS installation is not required.

## Memory Model

- `vault/Sources/` stores curated raw source notes.
- `vault/Wiki/` stores privacy-checked synthesized long-term memory.
- `vault/Wiki/index.md` is the navigation entrypoint.
- `vault/Wiki/log.md` is the audit trail.
- Claude-OS bootstraps a local wiki knowledge base and indexes `vault/Wiki/`;
  `vault/Sources/` is not bulk-ingested.

## Non-goals

- Do not vendor Claude-OS source into this repository.
- Do not make Qdrant, Ollama, or cloud exports mandatory for tests.
- Do not introduce student records, grades, diagnoses, parent communication, or
  sensitive individual cases.
- Do not include real memory data, Claude-OS databases, logs, uploads, or Redis
  state in release packages.

## Acceptance Criteria

- `teacher_tools.memory` manages deterministic source/wiki paths, slugs, index,
  log, and privacy-gated promotion.
- FastAPI exposes frontend-agnostic `/memory/...` endpoints.
- Default Compose includes Claude-OS core services and persistent `.claude-os/`
  storage.
- Claude-OS startup bootstraps a local project, wiki knowledge base, and
  `vault/Wiki/` autosync hook without indexing `vault/Sources/`.
- Release packages include runtime integration files and empty storage/vault
  skeletons only.
- Tests cover memory paths, index/log behavior, API behavior, privacy blocking,
  release boundaries, and Compose service presence.
