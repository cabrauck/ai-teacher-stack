# Tech Stack

## Current Runtime

- Python 3.12
- FastAPI
- Docker Compose
- `teacher_tools` service under `services/teacher_tools/`
- Claude-OS runtime service built from `brobertsaz/claude-os` at pinned commit
  `ee7b62bc5bf36541018a1c14592bcac2b59022f9`
- Redis for Claude-OS real-time learning queues
- Local files as primary state
- Obsidian-compatible Markdown in `vault/`
- Claude-OS local state under `.claude-os/`
- Markdown and DOCX output under `exports/` or lesson-specific vault folders
- Privacy-safe Schriftwesen generation under `teacher_tools.schriftwesen`

## Document Generation

- `python-docx` for DOCX export
- Markdown as the first-class authoring and inspection format
- OpenDocument Text (ODT) export as the planned open-format path for LibreOffice-compatible workflows
- PDF export later, after DOCX workflows are stable

## Development Tooling

- `pytest` for tests
- `ruff` for linting
- `uv` for Python dependency management
- Makefile commands from the repository root

## Optional Components

- Qdrant as an optional local vector store for retrieval experiments
- Ollama as optional local model runtime

## Frontend and Memory Shape

- Claude-OS MCP is the core memory service.
- `teacher_tools` exposes frontend-agnostic local APIs for lessons, exports,
  Schriftwesen, and memory vault operations.
- Teacher frontends can be Claude Code, Codex, a chat LLM, or a later UI.
- Later opt-in export adapters for BYCS or OneDrive
