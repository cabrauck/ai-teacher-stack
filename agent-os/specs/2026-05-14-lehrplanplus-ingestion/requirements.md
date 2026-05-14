# Requirements: LehrplanPLUS Ingestion

Status: Ready

## Purpose

Define the initial requirements for ingesting public LehrplanPLUS curriculum references into local structured records that can ground future lesson planning.

## Non-goals

- Do not ingest commercial textbook content.
- Do not require network access in tests.
- Do not mix generated lesson text into curriculum source records.

## Acceptance Criteria

- Requirements identify public curriculum source tracking as mandatory.
- Requirements require source URL and retrieval date for each ingested record.
- Requirements keep curriculum records separate from generated lesson content.
- Requirements preserve the v1 privacy boundary.

## Source Requirements

- Use official public LehrplanPLUS pages under `https://www.lehrplanplus.bayern.de/`.
- Start with Bayern Grundschule grade band 3/4.
- Do not ingest Servicematerialien, linked third-party resources, media, or commercial textbook material.
- Store source title, source URL, and retrieval date with every record.

## Data Requirements

- Produce structured JSON compatible with the current `CurriculumRecord` model unless implementation tests prove an optional extension is needed.
- Use deterministic ids derived from jurisdiction, school type, grade band, subject, and LehrplanPLUS section code.
- Keep records under `data/curriculum/` and separate from generated lesson output.

## Test Requirements

- Use local fixtures only; tests must not make HTTP calls.
- Cover parser normalization, deterministic ids, required source metadata, and existing search behavior.
