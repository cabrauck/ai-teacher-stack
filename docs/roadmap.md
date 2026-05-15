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
- [x] Add Claude-OS API/MCP runtime as the local memory service.
- [x] Add teacher-facing pre-release documentation.
- [x] Add LibreChat as the v1 teacher frontend.
- [x] Connect LibreChat to Claude-OS and teacher-tools through MCP.
- [x] Keep duplicate LibreChat RAG/vector/search services out of the default
  stack when Claude-OS provides the memory/knowledge path.

## Milestone 1.6: Claude-OS full runtime integration

- [ ] Expose the upstream Claude-OS UI as a documented local service.
- [ ] Keep the Claude-OS API/MCP endpoint separate from the Claude-OS UI URL.
- [ ] Report Claude-OS project, knowledge base, folder hook, document count,
  embedding coverage, jobs, Redis, Ollama, and frontend status in stack status.
- [ ] Prove that privacy-checked `vault/Wiki` pages sync into the Claude-OS
  wiki knowledge base and can be searched through Claude-OS MCP/API.
- [ ] Add explicit controls and documentation for vector search, hybrid search,
  reranking, and agentic RAG.
- [ ] Make memories, wiki pages, exported documents, Claude-OS KB status, and
  search results visible from LibreChat through teacher-facing tools or
  artifacts.
- [ ] Add Karpathy-style Obsidian wiki workflow docs: source ingest, wiki
  synthesis, query-to-wiki filing, index/log maintenance, and lint checks.
- [ ] Keep `vault/Sources/`, exports, credentials, and confidential school
  material out of default indexing.

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
- [ ] Evaluate browser preview for DOCX/PDF/ODT after LibreChat v1 stabilizes.

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

## Backlog Decisions

- [ ] Decide whether Open Design should become a teacher-facing branding tool
  for consistent worksheets, plans, board prompts, and export templates.
- [ ] Decide later whether Open Design should also support Vercel AI SDK v2
  frontend development.
- [ ] Build the v2 custom frontend with Vercel AI SDK after the LibreChat,
  Claude-OS, teacher-tools MCP, and preview workflows are stable.
