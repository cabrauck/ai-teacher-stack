# Architecture

## Design principle

This project is a local teacher workstation stack, not a central school platform.

The most important state is ordinary files:

- Markdown notes in an Obsidian vault
- structured curriculum JSON
- exported DOCX/PDF material
- optional local vector indexes

## Core components

### 1. Obsidian vault

The vault is the teacher's durable workspace:

```text
vault/
  Lehrplan/
  Unterricht/
  Materialien/
  Reflexion/
```

The AI stack should read and write Markdown here. Binary teaching material should remain local and should not be committed.

### 2. Teacher tools service

`services/teacher_tools` exposes local HTTP endpoints and will later expose equivalent MCP tools. The domain logic is kept pure so the same functions can be called from:

- FastAPI
- MCP
- CLI
- tests

### 3. Curriculum data

Curriculum data lives in `data/curriculum`. The sample file is only a placeholder.

Target structure:

```text
data/curriculum/
  bayern/
    grundschule/
      klasse_3_4/
        deutsch.json
        mathematik.json
        hsu.json
```

Each record should include:

- jurisdiction
- school type
- grade band
- subject
- learning area
- competency text
- content examples
- source URL
- source date

### 4. Document factory

The document factory converts structured lesson or worksheet objects into:

- Markdown
- DOCX
- later PDF

The first implementation uses `python-docx`.

### 5. Optional Ollama

Ollama is an optional local inference endpoint. The system must remain useful without it.

### 6. Optional RAG index

Qdrant is included behind a Docker Compose profile:

```bash
docker compose --profile rag up
```

Do not make Qdrant mandatory for simple workflows.

## Security and privacy

The public repo must contain no personal data, no secrets, and no proprietary teaching materials. Integrations with BYCS, OneDrive, or other storage systems must be opt-in and must not store tokens in the repository.
