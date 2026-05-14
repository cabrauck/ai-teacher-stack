# Document Output Standard

This standard applies to lesson plans, worksheets, solution keys, reflection notes, Markdown files, DOCX files, OpenDocument Text (ODT) files, and later PDF output.

## Output Order

- Markdown first.
- DOCX export required.
- ODT export allowed as the open document path for LibreOffice-compatible workflows.
- PDF later.

## File and Folder Conventions

- Use deterministic file names.
- Lesson folders should use names like `YYYY-MM-DD_SUBJECT_TOPIC`.
- Generated files should go to `exports/` or a lesson-specific vault folder.
- Filenames must not include student names or other personal data.
- Markdown should remain useful even when DOCX export fails.

## Review Requirement

All generated material must include a teacher-review note that makes clear the teacher must review, adapt, and approve the material before classroom use.

## Format Expectations

- Obsidian-compatible Markdown should be readable without a custom app.
- DOCX output should prioritize practical classroom structure over decorative formatting.
- ODT output should preserve the same classroom structure and review notes as DOCX when implemented.
- Generated lesson plans with curriculum references must expose those references in the output.
