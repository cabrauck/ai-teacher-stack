# LehrplanPLUS Ingestion - Shaping Notes

Status: Ready

## Scope

Plan official curriculum ingestion for Bayern Grundschule grade band 3/4, starting from public LehrplanPLUS Fachlehrplaene pages and the existing sample-data subjects.

## Decisions

- Store official source URLs with each ingested record.
- Store retrieval dates for traceability.
- Normalize data into local JSON under `data/curriculum/`.
- Keep the workflow independent from commercial textbook content.
- Do not ingest Servicematerialien, third-party links, media, or generated lesson text.
- Keep tests offline by using small local fixtures.

## Out of Scope

- Automatic recurring scraping.
- Commercial textbook ingestion.
- Runtime RAG changes.
- API changes before the curriculum model and tests are shaped.

## Product Alignment

Supports the v1 goal of curriculum grounding before generative lesson output.
