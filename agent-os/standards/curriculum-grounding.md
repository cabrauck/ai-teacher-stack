# Curriculum Grounding Standard

This standard applies to curriculum ingestion, curriculum search, lesson planning, and generated outputs that cite curriculum references.

## Rules

- Do not invent curriculum references.
- Store the source URL and retrieval date for ingested curriculum records.
- Prefer structured JSON records for curriculum data.
- Keep LehrplanPLUS ingestion separate from generated lesson content.
- Do not ingest commercial textbook content by default.
- Every lesson plan with curriculum references must expose those references in the output.

## Implementation Boundary

- Public curriculum records belong under `data/curriculum/`.
- Generated lesson content belongs under `exports/` or lesson-specific vault folders.
- Tests should use local fixtures and must not require network access.
