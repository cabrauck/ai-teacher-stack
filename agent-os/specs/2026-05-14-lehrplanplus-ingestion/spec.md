# Spec: LehrplanPLUS Ingestion

Status: Ready

## Purpose

Plan a controlled path from official public LehrplanPLUS curriculum pages to normalized local curriculum records for curriculum-grounded lesson planning.

## Source Scope and Licensing Assumptions

- Source scope is limited to official public LehrplanPLUS curriculum pages for Bayern Grundschule, grade band 3/4.
- Start with Fachlehrplaene pages such as `https://www.lehrplanplus.bayern.de/fachlehrplan/grundschule/3/mathematik` and the Grundschule index at `https://www.lehrplanplus.bayern.de/schulart/grundschule`.
- The official Impressum identifies ISB as responsible for the content and states that Lehrplan texts are not copyright-protected; other site content has additional usage limits and attribution requirements.
- Ingestion must target curriculum text and metadata only. Do not ingest Servicematerialien, linked third-party resources, media files, or commercial textbook content.
- Every ingested record must keep source title, source URL, and retrieval date.

## Normalized Record Model

Extend or preserve the current `CurriculumRecord` shape around these required fields:

- `id`: deterministic local id, for example `by-gs-3-4-mathematik-m3-4-1-1`.
- `jurisdiction`: `Bayern`.
- `school_type`: `Grundschule`.
- `grade_band`: `3/4`.
- `subject`: normalized subject display name.
- `learning_area`: LehrplanPLUS learning area code and title when available.
- `competency`: normalized competency expectation text.
- `content_examples`: list of content/example terms when present.
- `source`: object with `title`, `url`, and `retrieved_at`.

The first implementation may add optional fields only if tests show the current model cannot preserve required curriculum references without lossy parsing.

## Implementation Boundary

- Add ingestion as a local script or pure-function module boundary; basic lesson planning must not require network access.
- Parser tests must use local fixtures copied from small public curriculum excerpts, not live HTTP calls.
- Keep source curriculum records under `data/curriculum/`; generated lesson content remains under `exports/` or lesson-specific vault folders.
- Existing curriculum search should continue to load the current sample JSON during rollout.

## Non-goals

- Do not call external services from tests.
- Do not ingest commercial textbook content.
- Do not generate lesson plans as part of ingestion.
- Do not introduce student data fields.

## Acceptance Criteria

- The future implementation can store source URL and retrieval date with each curriculum record.
- Structured JSON records are preferred over ad hoc Markdown or plain text dumps.
- LehrplanPLUS source records remain separate from generated lesson content.
- Existing curriculum search behavior can remain functional during rollout.
- Lesson outputs that use curriculum references can expose those references.

## Test Plan

- Unit tests for parsing local LehrplanPLUS HTML/text fixtures into normalized records.
- Unit tests for deterministic ids and required source metadata.
- Regression tests for `load_curriculum_records`, `search_curriculum`, and `map_topic_to_curriculum`.
- Release boundary check after adding runtime files or docs.
