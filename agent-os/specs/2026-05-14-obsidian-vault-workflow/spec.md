# Spec: Obsidian Vault Workflow

Status: Draft

## Purpose

Plan a repeatable local vault workflow that connects lesson folders, curriculum references, generated documents, and anonymized teaching reflections in Obsidian-compatible Markdown.

## Non-goals

- Do not implement the vault workflow yet.
- Do not require Obsidian-specific plugins.
- Do not add Claude-OS memory extraction yet.
- Do not create structures for student records, grades, diagnoses, or parent communication.

## Acceptance Criteria

- Lesson folders can use names like `YYYY-MM-DD_SUBJECT_TOPIC`.
- Generated files can go to `exports/` or a lesson-specific vault folder.
- Markdown remains plain and readable.
- Lesson plans with curriculum references expose those references.
- Reflection notes stay anonymized and class-level.

## Initial Task List

- [ ] Confirm lesson folder naming convention.
- [ ] Shape Markdown metadata fields.
- [ ] Design lesson plan and reflection templates.
- [ ] Define how curriculum record links are represented.
- [ ] Plan tests for folder and file generation.
