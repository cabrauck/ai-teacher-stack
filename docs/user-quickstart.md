# ai-teacher-stack

This is the user runtime package for ai-teacher-stack. It contains the local
Docker Compose stack, sample curriculum data, prompts, templates, and empty
workspace folders for an Obsidian-compatible vault and exports.

Development tooling is not part of this package. Agent-OS files, specs, tests,
and repository-agent instructions live only in the GitHub repository.

## Requirements

- Docker Desktop or Docker Engine with Docker Compose
- A terminal in this extracted folder

## Start

```bash
cp .env.example .env
docker compose up --build
```

The local API listens on port `8010`.

Check the service:

```bash
curl http://localhost:8010/health
curl "http://localhost:8010/curriculum/search?q=lesen"
```

Generate an example lesson:

```bash
curl -X POST http://localhost:8010/lessons \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "HSU",
    "grade_band": "3/4",
    "topic": "Orientierung mit Karten",
    "duration_minutes": 45
  }'
```

Stop the stack:

```bash
docker compose down
```

## Local folders

- `data/curriculum/`: structured curriculum sample data
- `vault/`: Obsidian-compatible local notes skeleton
- `exports/`: generated documents
- `prompts/`: reusable planning and review prompts
- `templates/`: document templates

Run `scripts/init-vault.sh` if you want to create starter vault notes.

## Privacy boundary

Keep student names, grades, diagnoses, parent communication, credentials,
private school documents, and copyrighted textbook content out of this package
and out of any public repository. See `docs/privacy-boundary.md`.
