# Privacy boundary

## v1 allowed data

- public curriculum references
- generic lesson notes
- anonymized class-level reflections
- generated worksheets
- generated lesson plans
- weekly plans, daily organization plans, substitution notes, and anonymized handover notes without personal data
- privacy-checked Obsidian wiki memory notes under `vault/Wiki/`

## v1 excluded data

- student names
- grades
- diagnoses
- parent messages
- health information
- credentials or session tokens
- Student observation notes
- grades or Leistungsaufschreibungen
- diagnoses or health-related absence data
- parent communication with clear names
- raw source notes that have not been promoted through privacy validation must
  not be indexed by Claude-OS

## Public repository rule

The repository should contain only code, examples, and empty placeholders. Keep real classroom material local unless it is intentionally shareable.

## Claude-OS memory rule

Claude-OS is a core local runtime service, but it may index only
privacy-checked long-term memory under `vault/Wiki/`. Do not bulk-ingest
`vault/Sources/`, exports, real vault notes, credentials, or private school
documents. Claude-OS databases, logs, Redis state, uploads, and indexed
knowledge remain local under `.claude-os/` and must not be committed.
The automatic Claude-OS bootstrap configures only the `vault/Wiki/` hook.

The Claude-OS web UI in this pre-release is an admin and review surface only.
Do not treat it as a place to normalize sensitive student data or to browse raw
unreviewed source notes as if they were approved memory.
