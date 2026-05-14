# Privacy boundary

This project is designed to support compliance-conscious workflows under German
data protection expectations. It is not legal advice and does not claim
certified DSGVO, BSI IT-Grundschutz, or NIS2 compliance.

German data protection expectations are mandatory project policy. BSI and NIS2
are treated as best-effort engineering alignment targets: local-first storage,
data minimization, secure defaults, secret-free repository contents,
least-privilege configuration, explicit opt-in for cloud exports, and auditable
release boundaries.

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

Do not commit credentials, local `.env` files, BYCS or OneDrive tokens,
generated exports, real vault notes, Claude-OS databases, logs, Redis state,
uploads, or indexed knowledge content.

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

## Contributor rule

Any change touching privacy, cloud export, memory indexing, release packaging,
curriculum ingestion, vault structure, or security-sensitive behavior must
document the relevant risk and verification path in the Agent-OS spec or pull
request.
