# ByCS v1 Local Export

This package prepares local export packages for later manual use in ByCS. It
does not integrate with ByCS accounts or services.

## Purpose

ByCS v1 support is intentionally low-integrated. The AI Teacher Stack creates
clean local folders, manifests, and Office-compatible files that a teacher can
place in ByCS Drive, Spaces, Office, or Board workflows by hand or through a
ByCS Drive desktop sync folder.

## Explicit Non-Integration

- No OIDC or SSO.
- No automatic login.
- No ByCS API authentication.
- No scraping or browser automation.
- No automatic upload.
- No student data processing.
- No credentials in profiles or manifests.

## Recommended Workflow

1. Generate lesson material locally.
2. Export a Drive or Board package below `exports/bycs`.
3. Review the manifest and files.
4. Move or sync the package into the desired ByCS Drive or Spaces folder.
5. Open DOCX, XLSX, PPTX, or PDF files in ByCS Office where appropriate.
6. Use Board exports as Markdown/PDF/assets for manual Board preparation.

## Target Structure

Drive packages use folders like:

```text
exports/bycs/drive/2026-2027/Klasse_3a/HSU/2026-05-18_Kartenarbeit/
```

Spaces are represented as local target folders only:

```text
exports/bycs/spaces/2026-2027/class_space/Klasse_3a/
exports/bycs/spaces/2026-2027/teacher_team_space/Kollegium/
exports/bycs/spaces/2026-2027/subject_team_space/HSU_Team/
```

## Office-Compatible Formats

- DOCX: lesson plans, worksheets, solution keys, parent information drafts.
- XLSX: planning tables and lists without student data.
- PPTX: presentations, once a generator exists.
- PDF: final non-editable versions, once a generator exists or existing PDFs are
  copied into packages.
- Markdown: internal source where explicitly enabled.

The ByCS v1 layer models these targets and copies existing files. It does not
pretend to generate XLSX, PPTX, or PDF files when no generator exists.

## Board Export Concept

Board packages contain `tafelbild.md`, optional assets, and `manifest.json`.
The Markdown source is structured around:

- heading
- learning goal
- entry
- assignment
- consolidation
- memory note
- optional differentiation

There is no direct ByCS Board API integration in v1.

## Privacy Boundary

Exports are teacher-only and privacy-light. The validation layer blocks obvious
personal-data fields such as `student_name`, `birthdate`, `grade`,
`diagnosis`, and `parent_contact`. Manifests must not contain real student
data. Internal reflections are not copied into Drive packages unless explicitly
requested by code.

## CLI

```bash
python -m teacher_tools.bycs export-drive --input path/to/lesson.md --subject HSU --profile default
python -m teacher_tools.bycs export-board --input path/to/board.md --subject HSU --profile default
python -m teacher_tools.bycs validate-export exports/bycs/drive/2026-2027/Klasse_3a/HSU/package
```

`export-board` expects Markdown headings named `Lernziel`, `Einstieg`,
`Arbeitsauftrag`, `Sicherung`, and `Merksatz`.

## Later Roadmap

Possible later work, not implemented in v1:

- OIDC / SSO.
- Official ByCS API support if available and legally cleared.
- WebDAV or desktop-sync automation if permitted.
- Automatic uploads.
- Admin role and permission modeling.
- Learning-platform export.
- Messenger or email handoff.
- File-drop workflows.
- VIDIS or external education-service handoff.
