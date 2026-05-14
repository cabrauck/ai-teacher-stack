# Spec: ByCS v1 Local Export

Status: Done

## Purpose

Create a deliberately low-integration ByCS export layer that prepares local,
privacy-light, Office-compatible material packages for later manual placement
in ByCS Drive, Spaces, Office, or Board workflows.

## Non-goals

- Do not implement OIDC, SSO, automatic login, browser automation, scraping, or
  ByCS API authentication.
- Do not upload files automatically.
- Do not store credentials or account-specific ByCS settings.
- Do not process student names, grades, diagnoses, parent communication, or
  other sensitive student data.
- Do not depend on undocumented ByCS internals or proprietary import behavior.

## Acceptance Criteria

- A `teacher_tools.bycs` package models export profiles, local spaces, Office
  target file types, Drive packages, Board packages, and manifest metadata.
- Drive exports create deterministic local folders below `exports/bycs/drive`.
- Spaces are represented only as local folder concepts.
- Office compatibility is modeled for DOCX, XLSX, PPTX, and PDF without fake
  generators for unsupported outputs.
- Board exports create Markdown-first board packages with manifest metadata and
  optional asset copying.
- Export manifests omit personal student data and include a privacy status.
- Validation blocks or reports obvious personal-data fields.
- A minimal CLI can create Drive and Board packages from local Markdown files
  and validate an export package.
- Tests cover folder structure, manifest generation, space normalization,
  privacy validation, Office type mapping, and Board package structure.

## Initial Task List

- [x] Confirm low-integration ByCS boundary and non-goals.
- [x] Implement focused ByCS models and validation.
- [x] Implement Drive, Office, Spaces, and Board export helpers.
- [x] Add a minimal CLI under `python -m teacher_tools.bycs`.
- [x] Add example profile configuration without credentials.
- [x] Add export skeleton directories under `exports/bycs`.
- [x] Document workflow, privacy boundary, and later roadmap.
- [x] Run lint, tests, and release boundary check.
