# Architecture

## Purpose

This repository is a local workstation stack for teacher material planning.

## Main parts

- Obsidian-compatible Markdown vault in `vault/`
- Structured curriculum data in `data/curriculum/`
- Local Python service in `services/teacher_tools/`
- DOCX and Markdown exports in `exports/`
- Optional Qdrant profile for later RAG work
- Optional Ollama endpoint for local models

## Runtime

The first runtime is Docker Compose:

```bash
cp .env.example .env
docker compose up --build
```

The local API listens on port `8010`.

## Design notes

Keep domain logic in normal Python functions. FastAPI and future MCP wrappers should call the same functions.

Do not make the vector database or local LLM mandatory for basic lesson planning and export workflows.
