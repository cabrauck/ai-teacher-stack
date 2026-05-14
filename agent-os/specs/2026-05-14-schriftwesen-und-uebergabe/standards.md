# Standards

## privacy-boundary

- Schriftwesen may include only organizational, didactic, curriculum, and
  material information.
- Student names, observations, grades, diagnoses, illness data, parent
  communication, sensitive individual cases, and Leistungsaufschreibungen are
  outside v1.
- Claude-OS memory rules may be documented now, but active memory extraction
  remains later and opt-in.

## document-output

- Markdown remains the first-class output.
- DOCX export is required.
- Filenames must be deterministic and free of personal data.
- Generated Schriftwesen documents must include a teacher-review note.

## curriculum-grounding

- Schriftwesen may expose curriculum links.
- The system must not invent curriculum references.
- Missing curriculum references must be transparent and teacher-reviewable.

## python

- Domain logic stays in pure functions under `teacher_tools`.
- FastAPI remains a thin wrapper.
- Tests must cover non-trivial behavior.
- `ruff`, `pytest`, and release boundary checks must pass.

