# Privacy Boundary Standard

This standard applies to product docs, specs, examples, tests, generated material, release packages, and runtime features.

## Allowed in v1

- Public curriculum references
- Teacher-created generic lesson notes
- Generated worksheets
- Generated lesson plans
- Anonymized class-level reflections
- Weekly plans, daily organization plans, substitution plans, and anonymized handover notes without personal data
- Privacy-checked Obsidian wiki memory notes under `vault/Wiki/`

## Not Allowed in v1

- Student names
- Grades
- Diagnoses
- Parent messages
- Behavior incidents
- Health data
- Student observation notes
- Performance records or Leistungsaufschreibungen
- Private credentials
- School-internal confidential documents

## Rules

- Do not create forms, examples, prompts, schemas, or tests that make sensitive student data feel like a normal input.
- Do not store BYCS, OneDrive, model provider, or other private credentials in the repository.
- Use anonymized or generic classroom examples.
- Claude-OS is a core local memory service, but it may index only
  privacy-checked `vault/Wiki/` content.
- Keep cloud export integrations opt-in when they are added later.
