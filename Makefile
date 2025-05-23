.PHONY: dev format lint test deploy freeze login

export UV_PROJECT_ENVIRONMENT := src/venv

format:
	@uvx ruff format .

dev:
	@firebase emulators:start --only functions

lint:
	@uvx ruff check .

test:
	@uv run pytest

deploy:
	@firebase deploy --only functions

install:
	@uv pip install -e .
	@uv pip install -e '.[dev]'

uninstall:
	@uv pip uninstall .

tree:
	@tree -I 'build|__pycache__|*.egg-info'

freeze:
	@uv pip compile pyproject.toml > src/requirements.txt
	@#uv pip compile pyproject.toml --group dev

login:
	@uv run python ./src/main.py auth login