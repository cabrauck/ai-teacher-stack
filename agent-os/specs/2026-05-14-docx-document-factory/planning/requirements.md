# Requirements: DOCX Document Factory

Status: Planning

## Functional Requirements

- Export lesson plans as DOCX.
- Export worksheets as DOCX.
- Export solution keys as DOCX.
- Support OpenDocument Text (ODT) as an additional export format for LibreOffice-compatible open document workflows.
- Use Obsidian-compatible Markdown as a source where practical.
- Write generated documents to `exports/` by default.
- Use stable, descriptive filenames.

## Non-functional Requirements

- Keep document output readable and practical for classroom use.
- Keep the export path local-first.
- Keep tests offline.

## Non-goals

- No PDF requirement in the first implementation.
- ODT support must not replace required DOCX support.
- No cloud upload.
- No student-specific output.
