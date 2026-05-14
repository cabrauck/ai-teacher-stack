# Requirements: LehrplanPLUS Ingestion

Status: Ready

## Functional Requirements

- Capture official LehrplanPLUS references for Bayern Grundschule grade band 3/4.
- Start with a small subject set from the official Fachlehrplaene pages, prioritizing existing sample subjects.
- Preserve official source URLs.
- Preserve retrieval dates.
- Produce structured local JSON suitable for existing curriculum search.
- Keep source curriculum records separate from generated lesson content.

## Non-functional Requirements

- Work locally after data has been captured.
- Keep tests offline.
- Keep the data model small and inspectable.
- Avoid new runtime dependencies unless the parser cannot be implemented safely with the existing stack.

## Non-goals

- No student data.
- No commercial textbook content.
- No automatic cloud sync.
- No ingestion of Servicematerialien, third-party links, or media files.
