# Privacy boundary

## v1 allowed data

- public or officially permitted curriculum references
- teacher-created generic lesson notes
- anonymized class-level reflections
- generated worksheets
- generated lesson plans
- non-sensitive metadata

## v1 excluded data

- student names
- grades
- diagnoses
- parent messages
- behavior incidents
- health information
- private school-internal documents
- credentials or session tokens

## Implementation rule

If a feature needs identifiable student data, do not implement it in v1. Create an issue or TODO describing a future encrypted/private design instead.

## Public repository rule

This repo is intended to be public. Therefore:

- `vault/` contains only placeholders.
- `exports/` is ignored except `.gitkeep`.
- `.env` is ignored.
- binary files in the vault are ignored by default.
