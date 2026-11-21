.PHONY: build install test ruff-cs-check ruff-cs-fix ruff-linter-check ruff-linter-fix mypy-check check

build:
	docker build -t echo-bot .

install:
	uv sync --locked --only-dev

test:
	python3 -B -m unittest discover -s tests -v

ruff-cs-check:
	uv run --locked ruff format --check bot tests

ruff-cs-fix:
	uv run --locked ruff format bot tests

ruff-linter-check:
	uv run --locked ruff check bot tests

ruff-linter-fix:
	uv run --locked ruff check --fix bot tests

mypy-check:
	uv run --locked mypy

check: ruff-cs-check ruff-linter-check mypy-check test
