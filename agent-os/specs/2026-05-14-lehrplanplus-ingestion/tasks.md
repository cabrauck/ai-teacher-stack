# Tasks: LehrplanPLUS Ingestion

Status: Ready

## Purpose

Track implementation tasks for turning the ready LehrplanPLUS ingestion spec into a small, testable feature.

## Non-goals

- Do not add runtime dependencies before the feature spec is finalized.
- Do not make basic lesson planning depend on network access.

## Acceptance Criteria

- The source scope and normalized record model are fixed in `spec.md`.
- The task list includes local fixtures and tests.
- The task list preserves the privacy and curriculum-grounding standards.

## Planning Tasks

- [x] Confirm official source URLs and subject scope.
- [x] Define the normalized curriculum record model.
- [x] Design the ingestion command or script boundary.
- [x] Plan local fixtures for parser and normalization tests.

## Implementation Tasks

- [ ] Add local fixtures for parser and normalization tests.
- [ ] Implement parser and normalization as pure functions under `teacher_tools`.
- [ ] Add a local ingestion command or script that writes structured JSON records.
- [ ] Update curriculum search and mapping tests for ingested records.
- [ ] Document the workflow in repository docs.
- [ ] Run `uv run ruff check .`, `uv run pytest`, and the release boundary check.
