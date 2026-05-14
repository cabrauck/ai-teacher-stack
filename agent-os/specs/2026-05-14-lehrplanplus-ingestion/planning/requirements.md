# Requirements: LehrplanPLUS Ingestion

Status: Planning

## Functional Requirements

- Capture official LehrplanPLUS references for Bayern Grundschule grade band 3/4.
- Start with Deutsch, Mathe, and HSU.
- Preserve official source URLs.
- Preserve retrieval dates.
- Produce structured local JSON suitable for existing curriculum search.

## Non-functional Requirements

- Work locally after data has been captured.
- Keep tests offline.
- Keep the data model small and inspectable.

## Non-goals

- No student data.
- No commercial textbook content.
- No automatic cloud sync.
