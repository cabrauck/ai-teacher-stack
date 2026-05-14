# References for LehrplanPLUS Ingestion

## Repository Context

- `AGENTS.md` - coding conventions and privacy boundaries.
- `docs/roadmap.md` - Milestone 1 curriculum grounding items.
- `docs/privacy-boundary.md` - allowed and excluded data.
- `data/curriculum/bayern/grundschule/klasse_3_4/sample_curriculum.json` - current sample data shape.
- `services/teacher_tools/src/teacher_tools/curriculum.py` - current curriculum loading and search boundary.
- `services/teacher_tools/tests/test_curriculum.py` - existing curriculum test coverage.

## Official Source Context

- `https://www.lehrplanplus.bayern.de/schulart/grundschule` - Grundschule index and Fachlehrplaene entrypoint.
- `https://www.lehrplanplus.bayern.de/fachlehrplan/grundschule/3/mathematik` - example grade 3/4 Fachlehrplan page shape.
- `https://www.lehrplanplus.bayern.de/seite/impressum` - official responsibility, copyright, and usage notes.
