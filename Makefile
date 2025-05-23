.PHONY: dev format lint test deploy

format:
	@uvx ruff format .

dev:
	@firebase emulators:start --only functions

lint:
	@uvx ruff check .

test:
	@cd functions && uv run pytest -c pytest.ini

deploy:
	@firebase deploy --only functions