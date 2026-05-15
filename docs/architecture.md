# Architecture

## Purpose

This repository is a local workstation stack for teacher material planning.

## Main parts

- Obsidian-compatible Markdown vault in `vault/`
- LibreChat teacher frontend in `librechat`
- LibreChat MongoDB application-state service in `librechat-mongodb`
- Claude-OS core memory runtime in `claude-os` Docker service
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
`8010`. Claude-OS API/MCP listens on port `8051` and stores local runtime state
under `.claude-os/`.

The current pre-release keeps the teacher surface LibreChat-first:

- LibreChat on `http://localhost:3080` for normal teacher work
- Claude-OS API/MCP on `http://localhost:8051` for memory runtime integration
- `GET /status` on `teacher-tools` as the aggregated runtime readiness check

The upstream Claude-OS repository also contains a React/Vite management UI.
That UI is not yet exposed by this Docker Compose runtime. The planned
`claude-os-full-runtime` work will add a separate documented local URL for the
Claude-OS UI and keep it distinct from the API/MCP endpoint.

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

Current limitation: the runtime bootstraps the project and folder hook, but the
release does not yet prove document sync, embedding coverage, semantic search,
hybrid search, reranking, or agentic RAG through automated status checks. Those
items are tracked in the Claude-OS full runtime integration spec.

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
