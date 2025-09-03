.PHONY: \
	setup-local-environment \
	up \
	down \
	type-check \
	lint \
	sort-imports \
	migrate \
	makemigrations \
	clean-pyc \
	check \
	help \
	migrate-local \
	migrate-staging \
	makemigrations-local \
	makemigrations-staging \
	create-admin-user-local \
	create-admin-user-staging \
	setup-db-local \
	setup-db-staging \
	security-check

# Variables
COMPOSE_FILE = docker-compose.yaml
DOCKER_COMPOSE = docker compose -f $(COMPOSE_FILE)

# Virtual Environment
VENV_PATH = .venv
PIP = $(VENV_PATH)/bin/pip
PYTHON_VENV = $(VENV_PATH)/bin/python
RUFF = $(VENV_PATH)/bin/ruff
MYPY = $(VENV_PATH)/bin/mypy
ISORT = $(VENV_PATH)/bin/isort

setup-local-environment:  ## Setup local environment - virtual enviroment + dependencies
	( \
		rm -rf ${VENV_PATH}; \
		python3 -m venv ${VENV_PATH}; \
		${PYTHON_VENV} -m pip install -r requirements-dev.txt; \
	)

# env files
--check-local-env-file-exists-books:
	@if [ ! -f books-service/.env.local ]; then \
		echo "books-service/.env.local file not found! Please create it."; \
		exit 1; \
	fi

--check-local-env-file-exists-orders:
	@if [ ! -f orders-service/.env.local ]; then \
		echo "orders-service/.env.local file not found! Please create it."; \
		exit 1; \
	fi

--check-staging-env-file-exists:
	@if [ ! -f .env.staging ]; then \
		echo ".env.staging file not found! Please create it."; \
		exit 1; \
	fi

# Docker Compose commands
up: ## Start the Docker Compose services
	$(DOCKER_COMPOSE) up --build

down: ## Stop the Docker Compose services
	$(DOCKER_COMPOSE) down -v

restart: down up ## Restart services

logs: ## Show logs
	$(DOCKER_COMPOSE) logs -f

# Type checking
type-check: ## Run type checking
	$(MYPY) books-service/app
	$(MYPY) orders-service/app

# Linting
lint: ## Run linting checks using ruff
	$(RUFF) check books-service orders-service

# Imports checking
imports-check: ## Run imports checking using isort in check-only mode
	$(ISORT) --check-only --diff .

# Sorting imports
sort-imports: ## Sort imports using isort
	$(ISORT) .

# Cleanup
clean-pyc: ## Remove Python bytecode and cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/

# Full check
check: lint type-check sort-imports ## Run linting, type checking, testing, and sorting imports

# Ruff format
format: ## Run ruff to format code
	ruff format books-service orders-service
	ruff check --fix books-service orders-service

# Migrations by environment
migrate-books: ## Apply books-service migrations
	$(DOCKER_COMPOSE) exec books-service alembic upgrade head

migrate-orders: ## Apply orders-service migrations
	$(DOCKER_COMPOSE) exec orders-service alembic upgrade head

migrate-local: migrate-books migrate-orders  ## Apply all service migrations

makemigrations-books: ## Generate books-service migrations
	$(DOCKER_COMPOSE) exec books-service alembic revision --autogenerate -m "auto migration"

makemigrations-orders: ## Generate orders-service migrations
	$(DOCKER_COMPOSE) exec orders-service alembic revision --autogenerate -m "auto migration"

# Clean up docker system + volume
clean-docker-system: ## Removes docker data to start from scratch in your local
	docker system prune -a && \
	docker volume rm docker volume rm tepuii-api_postgres_data && \
	docker system prune -a

# Run unit tests
unit-tests: --check-local-env-file-exists-books
	export $(shell cat books-service/.env.local | xargs) && PYTHONPATH=books-service pytest books-service/tests/

# Help
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -vE '^--' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
