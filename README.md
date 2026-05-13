# ai-teacher-stack

Local-first AI teacher workspace for curriculum-grounded lesson planning, worksheet generation, Obsidian-based material memory, and optional local inference.

This repository is intentionally smaller than a full homelab AI platform. It is meant to run on a teacher workstation with Docker Compose and to be developed with Codex, Claude Code, or a comparable coding agent.

## Goals

- Run locally by default.
- Keep the Obsidian vault and generated documents on the user's machine.
- Start with teacher-only workflows, not student-data workflows.
- Ground lesson planning in structured curriculum data.
- Generate reusable Markdown, DOCX, and later PDF material.
- Support local Ollama when hardware allows it.
- Keep BYCS Drive, OneDrive, or other school cloud systems as export targets, not as the core runtime.

## Non-goals for v1

- No student accounts.
- No gradebook.
- No learner analytics.
- No automatic upload to school systems.
- No ingestion of commercial schoolbook PDFs by default.
- No sensitive student records in the public repo or default vault.

## Architecture

```text
Claude Code / Codex / terminal
        |
        v
local repo + Obsidian vault
        |
        +--> teacher-tools API / future MCP
        |       - search_curriculum
        |       - map_topic_to_curriculum
        |       - generate_lesson_plan
        |       - create_worksheet_markdown
        |       - export_lesson_docx
        |
        +--> local-rag / qdrant
        |
        +--> optional Ollama endpoint
        |
        +--> exports/
                - DOCX
                - Markdown
                - PDF later
```

## Repository layout

```text
.
├── AGENTS.md
├── CLAUDE.md
├── docker-compose.yml
├── .env.example
├── Makefile
├── data/curriculum/bayern/grundschule/klasse_3_4/sample_curriculum.json
├── docs/
├── prompts/
├── services/teacher_tools/
├── templates/docx/
├── vault/
└── scripts/
```

## Quickstart

```bash
cp .env.example .env
make check
make up
```

Check API:

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

## Codex workflow

Codex is best used here as a repository agent:

```bash
codex
```

Suggested first task:

```text
Read AGENTS.md and docs/architecture.md. Then implement the next TODO in docs/roadmap.md without adding student-data features.
```

## Create the public GitHub repository

This scaffold includes a bootstrap script:

```bash
./scripts/bootstrap-github-public.sh cabrauck ai-teacher-stack
```

Equivalent manual commands:

```bash
git init
git add .
git commit -m "Initial ai-teacher-stack scaffold"
gh repo create cabrauck/ai-teacher-stack --public --source=. --remote=origin --push
```

## Privacy boundary

The default scaffold is safe for a public repository because it contains only sample curriculum-style data and empty placeholder vault folders. Do not commit real student data, private BYCS/OneDrive files, tokens, exports, or non-public teaching materials.

## License

This project uses the **PolyForm Noncommercial License 1.0.0**.

That choice is intentional: the project should be easy to inspect, adapt, and share for noncommercial educational or personal use, while commercial use is not granted. This is not an OSI-approved open-source license.

Attribution is appreciated when you publish, teach with, or adapt the project. See `NOTICE.md` and `CITATION.cff`.
