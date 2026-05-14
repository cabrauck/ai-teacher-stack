# Requirements: DOCX Document Factory

Status: Draft

## Purpose

Define requirements for a local document factory that turns teacher-reviewed Markdown content into classroom-ready lesson plans, worksheets, and solution keys, with DOCX required and ODT planned for LibreOffice-compatible open document workflows.

## Non-goals

- Do not implement document generation in this placeholder spec.
- Do not make PDF export part of the first feature.
- Do not add cloud publishing or school platform upload behavior.
- Do not treat ODT support as a replacement for the required DOCX export.
- Do not include sensitive student data in generated filenames or content.

## Acceptance Criteria

- Requirements keep Markdown as the first inspectable format.
- Requirements make DOCX export mandatory for the feature.
- Requirements include ODT as an additional open-format export path.
- Requirements require deterministic filenames and teacher-review notes.
- Requirements keep generated files under `exports/` or lesson-specific vault folders.

## Initial Task List

- [ ] Confirm document types for the first factory pass.
- [ ] Define filename conventions.
- [ ] Define which document types need ODT output in the first open-format pass.
- [ ] Define required teacher-review note text or placement.
- [ ] Identify tests needed for generated DOCX behavior.
- [ ] Identify tests needed for generated ODT behavior.
