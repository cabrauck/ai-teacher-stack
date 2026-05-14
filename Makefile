.PHONY: check test lint release-check up down build init-vault tree

PYTHON ?= python

check: lint test release-check

lint:
	cd services/teacher_tools && uv run ruff check .

test:
	cd services/teacher_tools && uv run pytest

release-check:
	$(PYTHON) scripts/build_release.py --version dev --check

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

init-vault:
	./scripts/init-vault.sh

tree:
	find . -maxdepth 4 -type f | sort
