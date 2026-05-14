# Python Standard

This standard applies to Python code under `services/teacher_tools/` and to future Agent-OS specs that touch Python runtime behavior.

## Rules

- Keep domain logic in pure functions where possible.
- Keep FastAPI thin.
- Keep FastAPI request and response models under `teacher_tools/api.py`.
- Keep document export isolated under `teacher_tools/documents.py`.
- Keep curriculum loading and search isolated under `teacher_tools/curriculum.py`.
- Add tests for non-trivial behavior.
- Do not call external APIs in tests.
- Do not require Ollama for tests.
- Do not make Qdrant mandatory for basic flows.
- Run `ruff` and `pytest` before completing implementation work.

## Verification Commands

From `services/teacher_tools/`:

```bash
uv run ruff check .
uv run pytest
```
