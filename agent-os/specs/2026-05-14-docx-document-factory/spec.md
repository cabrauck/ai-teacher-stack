# Spec: DOCX Document Factory

Status: Draft

## Purpose

Plan a small local document factory for generating DOCX lesson plans, worksheets, and solution keys from inspectable Markdown-oriented content, with an additional OpenDocument Text (ODT) path for LibreOffice-compatible workflows.

## Non-goals

- Do not implement the document factory yet.
- Do not require PDF export.
- Do not add BYCS, OneDrive, or other publishing adapters.
- Do not make ODT replace DOCX as the required first classroom document format.
- Do not create student-specific documents or fields.

## Acceptance Criteria

- Markdown remains the first-class source or intermediate output.
- DOCX export is required for selected document types.
- ODT export is planned as an additional open-format output for LibreOffice-compatible workflows.
- Output filenames are deterministic and safe.
- All generated material includes a teacher-review note.
- Generated files go to `exports/` or a lesson-specific vault folder.

## Initial Task List

- [ ] Confirm lesson plan, worksheet, and solution key templates.
- [ ] Define deterministic filename rules.
- [ ] Define Markdown-to-DOCX conversion expectations.
- [ ] Define Markdown-to-ODT conversion expectations for open-format exports.
- [ ] Plan tests for document content and metadata.
- [ ] Document the future export workflow.
