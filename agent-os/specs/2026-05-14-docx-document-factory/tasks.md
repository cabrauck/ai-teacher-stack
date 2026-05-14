# Tasks: DOCX Document Factory

Status: Draft

## Purpose

Track initial implementation tasks for a later document factory feature with required DOCX output and an additional ODT path for LibreOffice-compatible open document workflows.

## Non-goals

- Do not implement DOCX changes during this Agent-OS bootstrap.
- Do not implement ODT changes during this Agent-OS bootstrap.
- Do not add PDF generation until it is promoted to its own work.
- Do not add cloud export behavior.

## Acceptance Criteria

- The task list starts with output shape and filename conventions.
- The task list includes focused tests for non-trivial document behavior.
- The task list keeps Markdown, DOCX, and open document output ahead of UI complexity.

## Initial Task List

- [ ] Confirm document types and filename conventions.
- [ ] Shape Markdown source conventions for lesson, worksheet, and solution output.
- [ ] Design export functions under the document boundary.
- [ ] Add tests for each planned document type.
- [ ] Implement DOCX generation for the selected outputs in a later feature pass.
- [ ] Add ODT generation for selected outputs after DOCX behavior is stable.
- [ ] Document the export workflow.
- [ ] Defer PDF export to a later spec.
