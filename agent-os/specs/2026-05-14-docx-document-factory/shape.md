# DOCX Document Factory - Shaping Notes

Status: Planning

## Scope

Plan DOCX outputs for lesson plans, worksheets, and solution keys, with Obsidian-compatible Markdown as a practical source format.

## Decisions

- Export generated documents to `exports/` by default.
- Use stable ASCII filenames without personal data.
- Treat PDF as a later export path.
- Keep document structure practical for classroom use before advanced styling.

## Out of Scope

- PDF generation in v1 document factory work.
- Direct upload to BYCS, OneDrive, or other school systems.
- Student-specific document generation.

## Product Alignment

Supports the v1 goal of Markdown and DOCX exports before UI complexity.
