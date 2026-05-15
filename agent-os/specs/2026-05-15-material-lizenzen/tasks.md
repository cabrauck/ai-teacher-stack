# Tasks: Materiallizenzen und Rechte-Metadaten

Status: Draft

## Purpose

Track research, shaping, and later implementation tasks for metadata-first
license handling around teaching materials.

## Research Tasks

- [ ] Research Germany school copying and digital teaching material baseline using official or authoritative sources such as schulbuchkopie.de, VG WORT, and official legal texts; summarize with links and no legal-advice claims.
- [ ] Research publisher license taxonomy for personal licenses, school licenses, copy templates, digital worksheets, platform access, and publisher AI-assistant boundaries; do not copy long publisher terms into the repo.
- [ ] Research OER and Creative Commons attribution models using UNESCO OER material, Creative Commons documentation, and German OER guidance.
- [ ] Identify common unresolved questions contributors should capture when publisher terms differ or are unclear.
- [ ] Prepare GitHub Issue descriptions for each research stream and add them to the `ai-teacher-stack Roadmap` project when the maintainer is ready.

## Spec Shaping Tasks

- [ ] Decide whether `LicenseMetadata` belongs in `teacher_tools.models`, a dedicated `teacher_tools.licensing` module, or both.
- [ ] Decide whether license metadata attaches first to lesson plans, generated material files, vault notes, export manifests, or only new document-factory outputs.
- [ ] Define the first accepted origin values: `teacher_created`, `oer`, `publisher_material`, `public_curriculum`, `unknown`.
- [ ] Define the default output-license behavior for teacher-created material with `CC-BY-SA-4.0`.
- [ ] Define warning behavior for missing or unknown metadata without presenting the system as legal advice.

## Later Implementation Tasks

- [ ] Add a small `LicenseMetadata` model with validation and tests.
- [ ] Render visible license metadata in lesson Markdown exports.
- [ ] Render visible license metadata in DOCX exports after Markdown behavior is stable.
- [ ] Add license metadata to vault note frontmatter or body sections where appropriate.
- [ ] Add license metadata to BYCS/export manifests without enabling autopublishing.
- [ ] Add release-boundary tests for any runtime templates or sample metadata included in user packages.

## Non-goals

- Do not implement legal-rights automation.
- Do not integrate publisher portals or BILDUNGSLOGIN.
- Do not ingest, index, copy, or redistribute publisher materials.
- Do not require network access for tests.
- Do not add student-specific or sensitive-data fields.
