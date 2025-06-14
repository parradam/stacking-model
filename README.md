# Ryan Comments
- repo structure
    - top-level src
    - two main dirs: stacking_model, tests
- cv
    - add uv
- repo commands
    - best: makefile or just
    - second-best: README.md
- gitignore
    - https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore

```bash
# Setup the local environment.
make setup

# Run the app locally.
make run

# Format source code and tests.
make format

# Lint source code and tests.
make lint

# Run tests.
make test

# Convenience target to format, lint, and test.
make validate

# Build a docker image for the app.
make docker-build

# Run a docker container for the app.
make docker-run
```