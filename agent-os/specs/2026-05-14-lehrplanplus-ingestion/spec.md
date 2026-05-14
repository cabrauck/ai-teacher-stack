# Spec: LehrplanPLUS Ingestion

Status: Draft

## Purpose

Plan a controlled path from official public LehrplanPLUS curriculum pages to normalized local curriculum records for curriculum-grounded lesson planning.

## Non-goals

- Do not implement the ingestion workflow yet.
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

## Initial Task List

- [ ] Confirm source scope and licensing assumptions.
- [ ] Define the normalized record model.
- [ ] Design parser and normalization boundaries.
- [ ] Create local fixtures for tests.
- [ ] Plan documentation for the ingestion workflow.
