# Roadmap

## Milestone 0: Scaffold

- [x] Local Docker Compose
- [x] FastAPI service
- [x] Sample curriculum
- [x] Markdown lesson generation
- [x] Basic DOCX export
- [x] Tests
- [x] Codex instructions

## Milestone 1: Core long-term memory

- [x] Add `vault/Sources/` for curated raw memory notes.
- [x] Add `vault/Wiki/` for privacy-checked synthesized memory.
- [x] Add local API operations for memory source notes, wiki pages, index, and promotion.
- [x] Add Claude-OS as a default Docker Compose runtime service.
- [x] Add Claude-OS Redis and persistent `.claude-os/` storage skeletons.
- [x] Add automatic Claude-OS KB bootstrap for `vault/Wiki/`.

## Milestone 1.5: Enduser pre-release

- [x] Add guided startup, stop, and readiness scripts for Windows and shell users.
- [x] Add an aggregated local stack status endpoint.
- [x] Position Claude-OS web UI as an admin and review surface.
- [x] Add teacher-facing pre-release documentation.
- [x] Add Claude Code and Codex App setup documentation with runtime-safe snippets.

## Milestone 2: Curriculum grounding

- [ ] Build official LehrplanPLUS ingestion script.
- [ ] Normalize Bayern Grundschule 3/4 records.
- [ ] Add source URLs and retrieval dates.
- [ ] Add tests for curriculum search and mapping quality.

## Milestone 2.5: Material licenses and rights metadata

- [ ] Shape the `material-lizenzen` Agent-OS spec.
- [ ] Define metadata categories for teacher-created material, OER, publisher material, public curriculum, and unknown sources.
- [ ] Use `CC-BY-SA-4.0` as the planned default when teachers choose to share or publish self-created material.
- [ ] Research German school copying and digital teaching material boundaries with official sources.
- [ ] Research publisher license categories without copying publisher terms or materials into the repository.
- [ ] Plan visible license metadata for Markdown, DOCX, vault notes, and export manifests.

## Milestone 3: Document factory

- [ ] Improve DOCX styling.
- [ ] Add OpenDocument Text (ODT) export path for LibreOffice-compatible workflows.
- [ ] Add worksheet export.
- [ ] Add solution-key export.
- [ ] Add visible license metadata once the Materiallizenzen model is implemented.
- [ ] Add PDF export path.

## Milestone 4: Schriftwesen and handover

- [x] Add weekly plan generation.
- [x] Add daily TOP generation.
- [x] Add substitution and mobile-reserve day information.
- [x] Add anonymized class handover summaries.
- [x] Validate all Schriftwesen documents before Markdown or DOCX export.

## Milestone 5: Optional local AI

- [ ] Add Ollama client for teacher-tools flows.
- [ ] Add hardware-aware model recommendations.
- [ ] Keep offline deterministic mode functional.

## Milestone 6: Export integrations

- [ ] Add disabled-by-default OneDrive adapter.
- [ ] Evaluate BYCS Drive sync options.
- [ ] Keep cloud exports manual or approval-gated.
