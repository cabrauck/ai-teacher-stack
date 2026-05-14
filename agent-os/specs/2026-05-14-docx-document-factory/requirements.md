# Requirements: DOCX Document Factory

Status: Draft

## Purpose

Define requirements for a local DOCX document factory that turns teacher-reviewed Markdown content into classroom-ready lesson plans, worksheets, and solution keys.

## Non-goals

- Do not implement document generation in this placeholder spec.
- Do not make PDF export part of the first feature.
- Do not add cloud publishing or school platform upload behavior.
- Do not include sensitive student data in generated filenames or content.

## Acceptance Criteria

- Requirements keep Markdown as the first inspectable format.
- Requirements make DOCX export mandatory for the feature.
- Requirements require deterministic filenames and teacher-review notes.
- Requirements keep generated files under `exports/` or lesson-specific vault folders.

## Initial Task List

- [ ] Confirm document types for the first factory pass.
- [ ] Define filename conventions.
- [ ] Define required teacher-review note text or placement.
- [ ] Identify tests needed for generated DOCX behavior.
