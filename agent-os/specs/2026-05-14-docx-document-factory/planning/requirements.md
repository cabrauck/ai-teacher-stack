# Requirements: DOCX Document Factory

Status: Planning

## Functional Requirements

- Export lesson plans as DOCX.
- Export worksheets as DOCX.
- Export solution keys as DOCX.
- Use Obsidian-compatible Markdown as a source where practical.
- Write generated documents to `exports/` by default.
- Use stable, descriptive filenames.

## Non-functional Requirements

- Keep document output readable and practical for classroom use.
- Keep the export path local-first.
- Keep tests offline.

## Non-goals

- No PDF requirement in the first implementation.
- No cloud upload.
- No student-specific output.
