# Tasks: LehrplanPLUS Ingestion

Status: Draft

## Purpose

Track the first implementation tasks for turning the draft LehrplanPLUS ingestion spec into a small, testable feature.

## Non-goals

- Do not implement ingestion as part of this Agent-OS bootstrap.
- Do not add runtime dependencies before the feature spec is finalized.
- Do not make basic lesson planning depend on network access.

## Acceptance Criteria

- The task list starts from source confirmation and data modeling.
- The task list includes local fixtures and tests.
- The task list preserves the privacy and curriculum-grounding standards.

## Initial Task List

- [ ] Confirm official source URLs and subject scope.
- [ ] Define or extend the curriculum record model.
- [ ] Design the ingestion command or script boundary.
- [ ] Add local fixtures for parser and normalization tests.
- [ ] Implement ingestion and normalization in a later feature pass.
- [ ] Update curriculum search tests in a later feature pass.
- [ ] Document the workflow in repository docs.
