# Requirements: LehrplanPLUS Ingestion

Status: Draft

## Purpose

Define the initial requirements for ingesting public LehrplanPLUS curriculum references into local structured records that can ground future lesson planning.

## Non-goals

- Do not implement ingestion in this placeholder spec.
- Do not ingest commercial textbook content.
- Do not require network access in tests.
- Do not mix generated lesson text into curriculum source records.

## Acceptance Criteria

- Requirements identify public curriculum source tracking as mandatory.
- Requirements require source URL and retrieval date for each ingested record.
- Requirements keep curriculum records separate from generated lesson content.
- Requirements preserve the v1 privacy boundary.

## Initial Task List

- [ ] Confirm official LehrplanPLUS source URLs and initial subject scope.
- [ ] Define the structured JSON record fields.
- [ ] Define local fixture expectations for parser tests.
- [ ] Decide where ingestion command documentation should live.
