# Standards for DOCX Document Factory

The following repository standards apply to future implementation work:

- `agent-os/standards/python.md`
- `agent-os/standards/privacy-boundary.md`
- `agent-os/standards/document-output.md`

Key implications:

- Keep export behavior isolated in `teacher_tools/documents.py`.
- Keep source Markdown useful even if DOCX export fails.
- Keep ODT output aligned with DOCX structure, review notes, and filename rules when implemented.
- Use stable filenames without student names or other personal data.
- Keep PDF as a later path unless a future spec promotes it.
