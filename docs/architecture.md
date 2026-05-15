# Architecture

## Purpose

This repository is a local workstation stack for teacher material planning.

## Main parts

- Obsidian-compatible Markdown vault in `vault/`
- LibreChat teacher frontend in `librechat`
- LibreChat MongoDB application-state service in `librechat-mongodb`
- Claude-OS core memory runtime in `claude-os` Docker service
- Claude-OS React/Vite management UI in `claude-os-frontend`
- Claude-OS Redis queue/cache service in `claude-os-redis`
- Structured curriculum data in `data/curriculum/`
- Local Python service in `services/teacher_tools/`
- DOCX and Markdown exports in `exports/`
- Schriftwesen workflow for weekly planning, daily organization, substitution, and anonymized handover
- teacher-tools MCP service for LibreChat tool access
- Optional Qdrant profile for later RAG work
- Optional Ollama endpoint for local models

## Runtime

The runtime is Docker Compose. It is intended to work on macOS through Docker
Desktop and on Windows through Docker Desktop with the WSL2 backend:

```bash
./scripts/start-pre-release.sh
```

LibreChat listens on port `3080`. The local teacher-tools API listens on port
`8010`. Claude-OS API/MCP listens on port `8051`. Claude-OS UI listens on port
`5173`. Claude-OS stores local runtime state under `.claude-os/`.

The current pre-release keeps the teacher surface LibreChat-first:

- LibreChat on `http://localhost:3080` for normal teacher work
- Claude-OS UI on `http://localhost:5173` for project, service, KB, and RAG
  review
- Claude-OS API/MCP on `http://localhost:8051` for memory runtime integration
- `GET /status` on `teacher-tools` as the aggregated runtime readiness check

The Claude-OS UI is intentionally separate from LibreChat and from the API/MCP
endpoint. LibreChat remains the teacher-facing workflow surface; Claude-OS UI is
an advanced local memory and runtime review surface.

## Long-term memory

Obsidian is the visible source of truth for teacher memory:

- `vault/Sources/`: curated raw notes
- `vault/Wiki/`: privacy-checked long-term memory for Claude-OS indexing
- `vault/Wiki/index.md`: navigation
- `vault/Wiki/log.md`: audit trail

Claude-OS indexes `vault/Wiki/` as the memory engine. LibreChat reaches
Claude-OS through MCP and does not run a separate default RAG/vector/search
stack for the same knowledge path. The Claude-OS Docker entrypoint
bootstraps an `ai-teacher-stack` project, a wiki knowledge base, and a
`project_memories` autosync hook for `/workspace/vault/Wiki`. The first sync is
best-effort and runs only when the configured local Ollama embedding model is
available.
Raw sources are not bulk ingested; promotion into the wiki must pass the shared
privacy validator.

The aggregated teacher-tools status reports Claude-OS API/UI reachability,
project bootstrap, wiki KB state, folder hook state, document and chunk counts,
recent jobs, service status, Ollama reachability, and missing local model names.
If Ollama or the configured embedding model is unavailable, the stack can still
start for non-RAG teacher workflows, but local-memory RAG capability is reported
as degraded.

## Design notes

Keep domain logic in normal Python functions. FastAPI and future MCP wrappers should call the same functions.

Do not make the vector database or local LLM mandatory for basic lesson planning and export workflows.

LibreChat is the v1 teacher frontend. Claude Code, Codex App, and similar
coding-agent clients are contributor tools, not product frontends or release
targets.

Schriftwesen is separate from reflection. It may store only organizational,
didactic, curriculum, and material information without student names,
observations, grades, diagnoses, parent communication, health data, or
performance records.
