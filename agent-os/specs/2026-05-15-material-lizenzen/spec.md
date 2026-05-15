# Spec: Materiallizenzen und Rechte-Metadaten

Status: Draft

## Purpose

Plan a small, local-first license metadata layer for teaching materials so the
stack can distinguish teacher-created material, OER, public curriculum
references, publisher material, and unknown sources before generated material is
exported or promoted into long-term memory.

The first increment is metadata-first. It does not implement legal automation,
publisher portal integration, Verlag catalog ingestion, or runtime enforcement.

## Background

The current roadmap prevents commercial textbook ingestion by default, but it
does not yet define how teachers should record rights metadata for materials
they create, reuse, reference, or export.

German school workflows can involve statutory copying rules, school or personal
publisher licenses, copy templates, digital worksheets, and OER licenses. These
contexts vary by source and license terms, so the stack needs transparent
metadata and teacher review instead of hidden assumptions.

## Initial Source Scope

- Start with Germany/Bayern-oriented school workflows because the existing
  curriculum grounding is centered on LehrplanPLUS.
- Treat public curriculum references as separate from generated material and
  publisher material.
- Treat self-created teacher material as eligible for a chosen output license.
- Use `CC-BY-SA-4.0` as the planned default for teacher-created material when
  the teacher wants to share or publish it.
- Treat publisher material as referential metadata only unless explicit rights
  are documented by the teacher.

## Planned Metadata Model

Plan a future `LicenseMetadata` model with at least these fields:

- `origin`: one of `teacher_created`, `oer`, `publisher_material`, `public_curriculum`, `unknown`.
- `license_id`: normalized id when available, for example `CC-BY-SA-4.0`.
- `license_name`: human-readable license or rights statement.
- `rights_holder`: author, publisher, institution, or rights holder when known.
- `source_url`: source or product URL when available.
- `retrieved_at`: retrieval date for online sources.
- `terms_url`: license terms or publisher usage terms URL when available.
- `attribution_text`: teacher-reviewable attribution string.
- `usage_scope`: short intended-use note such as local classroom use, school LMS, internal planning, or public OER sharing.
- `requires_teacher_review`: boolean, defaulting to true for non-public or unknown material.
- `notes`: unresolved rights or source questions.

The model should be optional in the first implementation pass and should not
break existing lesson, curriculum, export, Schriftwesen, or ByCS flows.

## Implementation Boundary

- No runtime API changes in this spec bootstrap.
- No external API calls or publisher portal access.
- No ingestion of publisher content, sample pages, worksheets, textbooks, or
  digital teaching products.
- No legal advice wording or certified compliance claims.
- No student data fields and no examples involving student names, grades,
  diagnoses, parent communication, performance records, or sensitive cases.

## Acceptance Criteria

- The roadmap includes a dedicated Materiallizenzen and rights-metadata stage
  before the document factory expands exports.
- A material licensing standard defines source categories, default license
  direction, publisher-material boundaries, and contributor research rules.
- Contributor research tasks are scoped so they can be filed as GitHub Issues
  without requiring private maintainer context.
- Future implementers have a clear draft metadata model and test direction.
- Existing runtime behavior remains unchanged.

## Open Questions

- Which publisher license categories are common enough to become first-class
  metadata values instead of free-text notes?
- Should license metadata live on lesson plans, individual materials, vault
  notes, export manifests, or all of them?
- How should teacher-selected output licenses interact with third-party sources
  embedded in the same material?
- Which attribution format should be used for OER and mixed-source exports?
- Should missing or unknown license metadata block exports later, or only render
  a visible warning?

## Test Plan

- Later unit tests for `LicenseMetadata` validation and allowed origin values.
- Later Markdown and DOCX tests proving that license blocks and teacher-review
  notes render together.
- Later privacy tests proving that license metadata does not introduce
  prohibited student-data fields.
- Release boundary check when templates, runtime docs, release files, or
  exported skeleton metadata are added.
