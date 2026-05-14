# Tech Stack

## Current Runtime

- Python 3.12
- FastAPI
- Docker Compose
- `teacher_tools` service under `services/teacher_tools/`
- Local files as primary state
- Obsidian-compatible Markdown in `vault/`
- Markdown and DOCX output under `exports/` or lesson-specific vault folders

## Document Generation

- `python-docx` for DOCX export
- Markdown as the first-class authoring and inspection format
- PDF export later, after DOCX workflows are stable

## Development Tooling

- `pytest` for tests
- `ruff` for linting
- `uv` for Python dependency management
- Makefile commands from the repository root

## Optional Components

- Qdrant as an optional local vector store for retrieval experiments
- Ollama as optional local model runtime

## Future Integration Shape

- Future MCP wrapper for structured tool access to teacher workflows
- Later opt-in export adapters for BYCS or OneDrive
- Later opt-in Claude-OS memory bridge after the vault workflow is stable
