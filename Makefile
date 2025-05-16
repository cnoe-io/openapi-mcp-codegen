# Makefile

.PHONY: build setup-venv activate-venv install run run-acp run-client langgraph-dev help

add-copyright-license-headers:
	@echo "Adding copyright license headers..."
	docker run --rm -v $(shell pwd)/openapi_mcp_codegen:/workspace ghcr.io/google/addlicense:latest -c "CNOE" -l apache -s=only -v /workspace

setup-venv:
	@echo "======================================="
	@echo " Setting up the Virtual Environment   "
	@echo "======================================="
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		echo "Virtual environment created."; \
	else \
		echo "Virtual environment already exists."; \
	fi

	@echo "======================================="
	@echo " Activating virtual environment       "
	@echo "======================================="
	@echo "To activate venv manually, run: source .venv/bin/activate"
	. .venv/bin/activate

	@echo "======================================="
	@echo " Installing dependencies with Poetry  "
	@echo "======================================="
	. .venv/bin/activate && poetry install

activate-venv:
	@echo "Activating virtual environment..."
	@if [ -d "venv" ]; then \
		. venv/bin/activate; \
	else \
		echo "Virtual environment not found. Please run 'make setup-venv' first."; \
	fi

install:
	@echo "======================================="
	@echo " Activating virtual environment and    "
	@echo " Installing poetry the current package "
	@echo "======================================="
	. .venv/bin/activate && poetry install

lint: setup-venv
	@echo "Running ruff..."
	. .venv/bin/activate && ruff check openapi_mcp_codegen tests

ruff-fix: setup-venv
	@echo "Running ruff and fix lint errors..."
	. .venv/bin/activate && ruff check openapi_mcp_codegen --fix

generate: setup-venv install
	@echo "Running the application with arguments: $(filter-out $@,$(MAKECMDGOALS))"
	. .venv/bin/activate && poetry run python -m openapi_mcp_codegen $(filter-out $@,$(MAKECMDGOALS))

# This rule allows passing arguments to the run target
%:
	@:

cz-changelog: setup-venv
	@echo "======================================="
	@echo " Checking and installing commitizen    "
	@echo "======================================="
	. .venv/bin/activate && pip show commitizen >/dev/null 2>&1 || pip install commitizen
	@echo "======================================="
	@echo " Generating changelog with cz-changelog"
	@echo "======================================="
	. .venv/bin/activate && cz bump --changelog


help:
	@echo "Available targets:"
	@echo "  setup-venv       Create virtual environment in .venv and install dependencies"
	@echo "  activate-venv    Activate the virtual environment"
	@echo "  install          Install the package"
	@echo "  run              Build, install, and run the application"
	@echo "  help             Show this help message"
