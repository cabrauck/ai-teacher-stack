# Material Licensing Standard

This standard applies to material sources, generated lesson material, vault
notes, exports, contributor research, examples, tests, and release packages.

## Compliance stance

The project does not provide legal advice and must not claim that a generated
material package is legally cleared for every classroom, platform, or publisher
license context.

License handling must support teacher review, transparent source metadata, and
local-first documentation of usage assumptions. Automated checks may warn about
missing metadata, but they must not replace publisher terms, school policy, or
legal review.

## Material source categories

Future material metadata should distinguish at least:

- `teacher_created`: material authored by the teacher or generated from teacher-owned prompts and public curriculum grounding.
- `oer`: openly licensed material such as Creative Commons material.
- `publisher_material`: material from textbook publishers, digital teaching products, workbooks, copy templates, or platform-specific offerings.
- `public_curriculum`: public curriculum references such as official LehrplanPLUS records.
- `unknown`: material whose origin or license cannot yet be determined.

## Required metadata direction

Non-trivial materials should be able to carry rights metadata including:

- origin category
- license id or license name
- rights holder or author when known
- source URL or bibliographic source when available
- retrieval date for online sources
- terms URL or publisher license reference when available
- attribution text
- intended usage scope
- teacher review status
- notes for unresolved questions

Missing metadata should remain visible and reviewable. Do not silently infer a
license for third-party material.

## Default for teacher-created material

When a teacher chooses to publish or share self-created material, the planned
default license option is `CC-BY-SA-4.0` unless the teacher explicitly selects a
different license or keeps the material private.

Generated exports should make the selected license visible once license
rendering is implemented.

## Publisher material boundary

Publisher material may be referenced and described for local planning, but the
repository must not ingest, copy, normalize, index, or redistribute copyrighted
publisher content without explicit usage rights.

Digital publisher works, school licenses, personal licenses, copy templates,
and platform-provided materials must be treated as license-specific. The system
may store teacher-entered metadata and review notes, but it must not assume that
a school license, personal license, or statutory classroom exception permits AI
upload, indexing, redistribution, or export.

## Contributor research rules

Contributor research must use official or authoritative sources where possible,
summarize findings in the contributor's own words, and link to sources. Do not
copy long publisher terms, textbook content, worksheets, sample pages, or other
copyrighted material into the repository.

Research deliverables should identify open questions separately from confirmed
facts and should avoid legal-advice wording.

## Release and privacy rules

User release packages may include empty metadata templates, sample OER-style
metadata, and documentation. They must not include real publisher material,
private classroom material, credentials, school-internal documents, or local
license account data.

License metadata must not normalize sensitive student data. If a material source
or attribution would require student names, grades, diagnoses, parent
communication, or other prohibited v1 data, it is out of scope for default
features.
