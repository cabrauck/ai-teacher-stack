# CLAUDE.md

Project memory for Claude Code, Claude-OS, or similar coding agents.

## Project intent

This is a local-first AI teacher workspace. It should help a teacher prepare, adapt, and export teaching material. It is not a school administration system and not a student-data platform.

## Strong preferences

- Keep the system understandable.
- Keep contributor setup IDE-agnostic: a cloned repository plus `.env`, `uv`,
  Docker Compose, and the documented checks should be enough to start.
- On Windows hosts, prefer an Ubuntu WSL2 checkout at `~/ai-teacher-stack` and
  treat it as the active workspace for agent and IDE work.
- Keep LibreChat as the v1 teacher frontend while preserving local file
  workflows for durable state and exports.
- Use Obsidian-compatible Markdown for durable memory.
- Treat Claude-OS as the core local memory runtime over `vault/Wiki/`.
- Keep Obsidian as the human-readable source of truth for teacher memory.
- Treat DOCX export as a first-class feature.
- Keep Cloud, BYCS, and OneDrive integrations optional and off by default.
- Keep local Ollama optional because teacher hardware varies.
- Treat Schriftwesen as a core module, separate from reflection.

## Default workflow

1. Read or create a planning note in `vault/Unterricht/`.
2. Search curriculum data in `data/curriculum/`.
3. Generate a structured lesson plan as Markdown.
4. Export DOCX into `exports/`.
5. Add a reflection note after use.

Long-term memory workflow:

1. Capture curated raw notes in `vault/Sources/`.
2. Promote only privacy-checked synthesis into `vault/Wiki/`.
3. Keep `vault/Wiki/index.md` and `vault/Wiki/log.md` current.
4. Let Claude-OS index `vault/Wiki/`; do not bulk-ingest raw sources.

Schriftwesen workflow:

1. Create weekly plans, daily TOP plans, substitution notes, or anonymized handover notes in `vault/Schriftwesen/`.
2. Keep templates under `vault/Templates/Schriftwesen/`.
3. Store only organizational, didactic, curriculum, and material information.
4. Validate privacy before export or any later memory use.

## Agent-OS workflow

For larger development changes, read `agent-os/product/`, relevant
`agent-os/standards/`, and the matching spec under `agent-os/specs/` before
implementation. Implement only from specs marked `Ready` or `In Progress`.
Agent-OS is developer-only planning context and must stay out of user release
packages.
Agent-OS is the dev gate only. It is separate from the teacher frontend and from
the Claude-OS runtime memory service.

Contributors may propose roadmap changes through issues, specs, or pull
requests. Maintainer review owns final roadmap direction, milestone priority,
and release timing.

GitHub Project `ai-teacher-stack Roadmap` is the visible coordination board for
open roadmap issues, spec shaping, implementation status, and PR review flow.
Agent-OS remains the decision and specification layer for larger changes.

Use `CONTRIBUTING.md`, `docs/contributor-setup.md`, and the
`contributor-workflow` Agent-OS standard for contributor onboarding. Use the
`security-compliance` standard for privacy, security, cloud export, release
boundary, memory indexing, and incident-sensitive changes.

## Privacy rule

Do not create structures that make it natural to store identifiable student data. Use anonymized class-level notes only in examples.

Remember: Im ai-teacher-stack ist Schriftwesen ein Kernmodul. Es umfasst Wochenplan, TOP/Tagesorganisationsplan, Vertretungsplan und anonymisierte Übergabeunterlagen. Claude-OS darf daraus nur nicht-personenbezogene organisatorische, didaktische und materialbezogene Informationen speichern. Schülerbeobachtungen, Namen, Noten, Diagnosen, Krankheitsdaten, Elternkommunikation und sensible Einzelfälle dürfen nicht in Claude-OS, RAG, Logs, `vault/Wiki/` oder project_memories übernommen werden.

The project is designed to support compliance-conscious workflows under German
data protection expectations. It does not claim certified DSGVO, BSI
IT-Grundschutz, or NIS2 compliance. BSI and NIS2 are best-effort engineering
alignment targets, not certification claims.
