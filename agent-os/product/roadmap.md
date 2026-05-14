# Roadmap

Agent-OS stays a developer/specification layer. It becomes productive-light starting with the first real feature spec: `lehrplanplus-ingestion`.

## v0.1 Scaffold Stabilization

- Stabilize the repository layout, Docker Compose runtime, Makefile commands, and `teacher_tools` service boundary.
- Keep release packages focused on runtime files, sample data, prompts, templates, empty vault/export skeletons, and user documentation.
- Keep Agent-OS, tests, specs, and development-only metadata out of end-user release packages.

## v0.2 LehrplanPLUS Ingestion

- Define a controlled ingestion workflow for public LehrplanPLUS curriculum references.
- Store source URL and retrieval date with normalized records.
- Keep ingestion data separate from generated lesson content.
- Use this as the first productive-light Agent-OS feature spec: `lehrplanplus-ingestion`.

## v0.3 DOCX Document Factory

- Expand DOCX export into a small document factory for lesson plans, worksheets, and solution keys.
- Add an OpenDocument Text (ODT) export path for LibreOffice-compatible open document workflows while keeping DOCX required.
- Keep Markdown as the inspectable source or intermediate format.
- Use deterministic filenames and teacher-review notes.

## v0.4 Obsidian Vault Workflow

- Define lesson folder conventions such as `YYYY-MM-DD_SUBJECT_TOPIC`.
- Connect lesson notes, curriculum references, generated files, and anonymized reflection notes.
- Keep files readable as plain Obsidian-compatible Markdown.

## v0.5 Optional Local AI/Ollama Support

- Add optional local AI workflows through Ollama only after core deterministic flows are stable.
- Do not require Ollama for tests, bootstrap, or basic lesson export.
- Keep generated output curriculum-grounded and teacher-reviewed.

## Later: Claude-OS Memory Bridge

- Explore a privacy-filtered bridge from Obsidian reflections into Claude-OS memory.
- Keep this opt-in and separate from v1 runtime behavior.

## Later: BYCS/OneDrive Export Adapters

- Consider explicit export adapters for BYCS or OneDrive.
- Keep adapters disabled by default and avoid autopublishing.
- Do not store credentials or school-internal confidential documents in the repository.

## Out of Scope

- Student accounts, gradebooks, learner analytics, parent communication, behavior incident records, or central multi-user school platform features.
- Commercial textbook ingestion by default.
