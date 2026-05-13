# CLAUDE.md

Project memory for Claude Code or similar coding agents.

## Project intent

This is a local-first AI teacher workspace. It should help a teacher prepare, adapt, and export teaching material. It is not a school administration system and not a student-data platform.

## Strong preferences

- Keep the system understandable.
- Prefer local file workflows over a large web UI.
- Use Obsidian-compatible Markdown for durable memory.
- Treat DOCX export as a first-class feature.
- Keep Cloud/BYCS/OneDrive integrations optional and off by default.
- Keep local Ollama optional because teacher hardware varies.

## Default workflow

1. Read or create a planning note in `vault/Unterricht/`.
2. Search curriculum data in `data/curriculum/`.
3. Generate a structured lesson plan as Markdown.
4. Export DOCX into `exports/`.
5. Add a reflection note after use.

## Privacy rule

Do not create structures that make it natural to store identifiable student data. Use anonymized class-level notes only in examples.
