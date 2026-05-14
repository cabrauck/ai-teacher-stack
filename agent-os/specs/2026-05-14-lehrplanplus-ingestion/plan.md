# LehrplanPLUS Ingestion Plan

Status: Ready

## Goal

Create an implementation path for ingesting official LehrplanPLUS curriculum references into local structured data without making basic lesson planning depend on network access.

## Plan Shape

- Use official public LehrplanPLUS pages for Bayern Grundschule 3/4 as the source scope.
- Keep ingestion focused on curriculum text and metadata, not Servicematerialien or third-party links.
- Preserve source title, source URL, and retrieval date on every record.
- Implement parsing and normalization with local fixtures and offline tests.
- Keep generated lesson content separate from source curriculum records.

## Current Decision

This spec is ready for implementation. The next pass should add fixtures, parser/normalization functions, a local ingestion script or command, tests, and workflow documentation.
