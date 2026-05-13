.PHONY: check test lint up down build init-vault tree

check: lint test

lint:
	cd services/teacher_tools && uv run ruff check .

test:
	cd services/teacher_tools && uv run pytest

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
