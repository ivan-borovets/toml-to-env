# Makefile variables
PYTHON := python
DOCKER_COMPOSE := docker compose
DOCKER_COMPOSE_FILE := docker-compose.yaml

SCRIPTS_DIR := scripts
TESTS_DIR := tests
PRINT_ENVS_SCRIPT := $(SCRIPTS_DIR)/makefile/print_envs.py

# Setting environment
.PHONY: env.dev env.prod env.which

env.dev:
	@$(PYTHON) $(PRINT_ENVS_SCRIPT) development

env.prod:
	@$(PYTHON) $(PRINT_ENVS_SCRIPT) production

env.which:
	@echo APP_ENV=$(APP_ENV)

# Source code formatting
.PHONY: code.format code.lint code.test code.cov code.check

code.format:
	isort $(SCRIPTS_DIR) $(TESTS_DIR)
	black $(SCRIPTS_DIR) $(TESTS_DIR)

code.lint: code.format
	bandit -r $(SCRIPTS_DIR) -c pyproject.toml
	ruff check $(SCRIPTS_DIR)
	pylint $(SCRIPTS_DIR)
	mypy $(SCRIPTS_DIR)

code.test:
	pytest -v

code.cov:
	coverage run -m pytest
	coverage report

code.cov.html:
	coverage run -m pytest
	coverage html

code.check: code.lint code.test

# Docker Compose controls
.PHONY: up.db up.db-echo down down.total

up.db:
	@echo "APP_ENV=$(APP_ENV)"
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d app_db_pg --build

up.db-echo:
	@echo "APP_ENV=$(APP_ENV)"
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up app_db_pg --build

down:
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

down.total:
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v
