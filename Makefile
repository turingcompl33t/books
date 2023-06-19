# Makefile

# -----------------------------------------------------------------------------
# Script Execution
# -----------------------------------------------------------------------------

# Create a new entry
new:
	python _script/new.py --books books --templates _template $(name)

migrate:
	python _script/migrate_0.py --path books --verbose

# -----------------------------------------------------------------------------
# Source Quality Assurance
# -----------------------------------------------------------------------------

.PHONY: isort
isort:
	isort --profile black --line-length 80 _script/*.py

.PHONY: format
format:
	black --line-length 80 _script/*.py

.PHONY: lint
lint:
	flake8 _script/*.py

.PHONY: qa
qa: isort format lint