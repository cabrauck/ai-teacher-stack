# Tasks: DOCX Document Factory

Status: Draft

## Purpose

Track initial implementation tasks for a later DOCX document factory feature.

## Non-goals

- Do not implement DOCX changes during this Agent-OS bootstrap.
- Do not add PDF generation until it is promoted to its own work.
- Do not add cloud export behavior.

## Acceptance Criteria

- The task list starts with output shape and filename conventions.
- The task list includes focused tests for non-trivial document behavior.
- The task list keeps Markdown and DOCX ahead of UI complexity.

## Initial Task List

- [ ] Confirm document types and filename conventions.
- [ ] Shape Markdown source conventions for lesson, worksheet, and solution output.
- [ ] Design export functions under the document boundary.
- [ ] Add tests for each planned document type.
- [ ] Implement DOCX generation for the selected outputs in a later feature pass.
- [ ] Document the export workflow.
- [ ] Defer PDF export to a later spec.
