# Spec: Schriftwesen und Uebergabe

Status: Done

## Purpose

Add a privacy-safe Schriftwesen module for weekly planning, daily organization,
substitution planning, mobile-reserve-compatible day information, and anonymized
handover summaries.

Schriftwesen is a v1 core module and must not be hidden under reflection. It
supports practical classroom planning and handover while keeping the v1
no-student-data boundary intact.

## Sources and Rationale

- LDO section 3 requires careful preparation, balanced distribution of teaching
  content and assessments, and plans or evidence of covered teaching content
  when required in individual cases.
- The 2023 KMS on official Schriftwesen at Grund- and Mittelschulen reduces
  routine paperwork and routine submission duties, but does not remove the
  preparation and documentation duty.
- Weekly plans are a didactically established format for differentiated work.
- TOP is treated as a practical daily organization format, not as a statewide
  official standard term.

## Non-goals

- Do not store student names, grades, diagnoses, illness data, parent
  communication, sensitive individual cases, student observation notes, or
  Leistungsaufschreibungen.
- Do not activate Claude-OS memory extraction.
- Do not add a separate MCP runtime yet; future MCP wrappers should call the
  same pure functions as FastAPI.
- Do not add automatic school-cloud upload.

## Acceptance Criteria

- Weekly plans, daily TOP plans, substitution plans, and anonymized handover
  summaries can be generated through pure functions and FastAPI endpoints.
- Schriftwesen documents can be rendered as Obsidian-compatible Markdown and
  exported as DOCX.
- All Schriftwesen documents include `personenbezogene_daten: false` and a
  teacher-review note.
- A neutral privacy validator blocks obvious personal-data fields and explicit
  personal-data markers before export or later memory use.
- ByCS export privacy validation continues to work through a compatibility
  wrapper.
- Vault skeletons and runtime templates are included in user release packages;
  Agent-OS and dev files remain excluded.

