# --- Globals
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

PROJECT_NAME := example_repo

SRC := $(PROJECT_NAME)
TESTS := tests

DOCKER_IMAGE_TAG := $(PROJECT_NAME):local

# --- Environment Variables
export PYTHONUNBUFFERED := 1
export PYTHONPATH := $(ROOT_DIR)

# --- Targets
.PHONY: setup
setup:
	uv sync --extra dev

.PHONY: run
run:
	uv run python -m $(PROJECT_NAME)

.PHONY: format
format:
	uv run ruff format $(SRC) $(TESTS)

.PHONY: lint
lint:
	uv run ruff format --check $(SRC) $(TESTS)
	uv run ruff check $(SRC) $(TESTS)
	uv run mypy $(SRC) $(TESTS)

.PHONY: test
test:
	uv run pytest ${TESTS}

.PHONY: test
validate: format lint test

.PHONY: docker-build
docker-build:
	docker build -t $(DOCKER_IMAGE_TAG) -f Dockerfile .

.PHONY: docker-run
docker-run:
	docker run -it --rm $(DOCKER_IMAGE_TAG)