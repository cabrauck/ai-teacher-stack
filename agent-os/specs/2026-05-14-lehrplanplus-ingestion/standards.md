# Standards for LehrplanPLUS Ingestion

The following repository standards apply to future implementation work:

- `agent-os/standards/python.md`
- `agent-os/standards/privacy-boundary.md`

Key implications:

- Keep curriculum loading and search isolated in `teacher_tools/curriculum.py`.
- Tests must not call external APIs.
- Store only public curriculum references and metadata.
- Do not ingest copyrighted textbook content.
