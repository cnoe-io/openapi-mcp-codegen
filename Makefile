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
	@echo " Adding pip as a Poetry dependency    "
	@echo "======================================="
	. .venv/bin/activate && poetry add pip --dev

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
	. .venv/bin/activate && pip show commitizen >/dev/null 2>&1 || . .venv/bin/activate && pip install -U commitizen
	@echo "======================================="
	@echo " Generating changelog with cz-changelog"
	@echo "======================================="
	. .venv/bin/activate && cz bump --changelog

# test_Makefile

.PHONY: test test-venv

test-venv:
	@echo "======================================="
	@echo " Setting up test virtual environment   "
	@echo "======================================="
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		echo "Test virtual environment created."; \
	else \
		echo "Test virtual environment already exists."; \
	fi
	@echo "======================================="
	@echo " Installing test dependencies         "
	@echo "======================================="
	. .venv/bin/activate && pip install -U pip pytest && poetry install

test: test-venv
	@echo "======================================="
	@echo " Running pytest on tests directory     "
	@echo "======================================="
	. .venv/bin/activate && pytest tests


help:
	@echo "Available targets:"
	@echo "  add-copyright-license-headers  Add copyright license headers to source files"
	@echo "  setup-venv                     Create virtual environment in .venv and install dependencies"
	@echo "  activate-venv                  Activate the virtual environment"
	@echo "  install                        Install the package"
	@echo "  lint                           Run ruff linter on codebase"
	@echo "  ruff-fix                       Run ruff and fix lint errors"
	@echo "  generate [ARGS]                Build, install, and run the application with optional arguments"
	@echo "  cz-changelog                   Generate changelog using commitizen"
	@echo "  help                           Show this help message"
