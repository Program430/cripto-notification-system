COMPOSE_PROD=docker compose
COMPOSE_LOCAL=docker compose -f docker-compose.yml -f docker-compose.local.yml

.PHONY: prod-up prod-down
.PHONY: dev-up dev-down
.PHONY: test test-unit test-integration lint typecheck check

prod-up:
	$(COMPOSE_PROD) up -d --build

prod-down:
	$(COMPOSE_PROD) down

dev-up:
	$(COMPOSE_LOCAL) up --build

dev-down:
	$(COMPOSE_LOCAL) down

test:
	poetry run pytest

test-unit:
	poetry run pytest tests/unit

test-integration:
	poetry run pytest tests/integration

lint:
	poetry run ruff check .

typecheck:
	poetry run mypy src

check: lint typecheck test
