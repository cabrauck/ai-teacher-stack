# Security and Compliance Standard

This standard applies to product docs, specs, runtime features, examples,
tests, release packaging, integrations, and contributor workflows.

## Compliance stance

The project is designed to support compliance-conscious workflows under German
data protection expectations. It does not claim certified DSGVO, BSI
IT-Grundschutz, or NIS2 compliance.

German data protection expectations are mandatory project policy. BSI and NIS2
are best-effort engineering alignment targets.

## Required privacy baseline

Default project behavior must avoid:

- student names
- grades
- diagnoses
- health data
- parent communication
- behavior incidents
- performance records or Leistungsaufschreibungen
- credentials and session tokens
- confidential school-internal documents
- copyrighted textbook content without usage rights

Use only public curriculum references, generic lesson material, anonymized
class-level notes, and privacy-checked Obsidian wiki memory in default
features, docs, examples, tests, and release packages.

## German data protection expectations

Design decisions must support data minimization, purpose limitation, local-first
storage, transparency, teacher review, and separation between public repository
content and private local material.

Deployment context can trigger additional requirements under DSGVO/GDPR, BDSG,
state data protection law, school law, and local school authority policies. The
repository must not present itself as legal advice or as sufficient by itself
for institutional compliance.

## BSI and NIS2 best-effort alignment

Use these engineering practices where relevant:

- secure defaults
- least-privilege configuration
- explicit opt-in for cloud exports and integrations
- no secrets in repository files, examples, logs, or tests
- dependency hygiene and reproducible local setup
- auditable release boundaries
- local runtime state excluded from commits
- documented security and incident considerations in specs and PRs
- clear separation between runtime user packages and development-only tooling

## Runtime and release rules

- Local files and the Obsidian vault remain the primary state.
- Cloud export adapters must be disabled by default and approval-gated when
  added.
- Claude-OS may index only privacy-checked `vault/Wiki/` content.
- User release packages must not contain Agent-OS, specs, tests, `.claude/`,
  `.github/`, local `.env`, generated exports, vault content, credentials,
  Claude-OS databases, logs, Redis state, uploads, or indexed knowledge.

## Review expectations

Any change touching privacy, security, cloud export, memory indexing, release
packaging, curriculum ingestion, or vault structure must document the relevant
risks and verification path in the spec or pull request.
