# Standards for LehrplanPLUS Ingestion

The following repository standards apply to future implementation work:

- `agent-os/standards/python.md`
- `agent-os/standards/privacy-boundary.md`
- `agent-os/standards/curriculum-grounding.md`

Key implications:

- Keep curriculum loading and search isolated in `teacher_tools/curriculum.py`.
- Tests must not call external APIs.
- Store only public curriculum references and metadata.
- Store source URL and retrieval date for ingested curriculum records.
- Do not ingest copyrighted textbook content.
