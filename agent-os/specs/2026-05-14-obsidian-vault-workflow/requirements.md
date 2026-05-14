# Requirements: Obsidian Vault Workflow

Status: Draft

## Purpose

Define requirements for a local Obsidian-compatible vault workflow that organizes lesson planning notes, curriculum references, generated files, and anonymized reflection notes.

## Non-goals

- Do not implement vault automation in this placeholder spec.
- Do not add Claude-OS memory integration yet.
- Do not add student records or student-specific note structures.
- Do not require an Obsidian plugin.

## Acceptance Criteria

- Requirements define lesson folders using names like `YYYY-MM-DD_SUBJECT_TOPIC`.
- Requirements keep Markdown readable without custom tooling.
- Requirements connect generated files to lesson-specific vault folders where appropriate.
- Requirements preserve the v1 privacy boundary.

## Initial Task List

- [ ] Confirm lesson folder naming convention.
- [ ] Define required Markdown files and metadata fields.
- [ ] Define how curriculum references appear in lesson notes.
- [ ] Identify tests for folder and file generation.
