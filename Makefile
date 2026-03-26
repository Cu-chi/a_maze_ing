PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
--disallow-untyped-defs --check-untyped-defs
VENV = .venv

install:
	poetry install

run:
	poetry run $(PYTHON) $(MAIN) $(CONFIG)

debug:
	poetry run $(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	@clean: @rm -rf $$(find . -type d -name "__pycache__") $$(find . -type d -name ".mypy_cache")_

lint:
	poetry run $(PYTHON) -m flake8 . --exclude $(VENV)
	poetry run $(PYTHON) -m mypy . $(MYPY_FLAGS)

lint-strict:
	poetry run $(PYTHON) -m flake8 . --exclude $(VENV)
	poetry run $(PYTHON) -m mypy . $(MYPY_FLAGS) --strict

build-mazegen:
	cd mazegen_lib; poetry build

.PHONY: install run debug clean lint lint-strict build-mazegen
