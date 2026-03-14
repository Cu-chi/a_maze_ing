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
	@rm -rf __pycache__ .mypy_cache maze.txt **/__pycache__ **/.mypy_cache \
	**/**/__pycache__ maze.txt

lint:
	$(PYTHON) -m flake8 . --exclude $(VENV)
	$(PYTHON) -m mypy . $(MYPY_FLAGS)

lint-strict:
	$(PYTHON) -m flake8 . --exclude $(VENV)
	$(PYTHON) -m mypy . $(MYPY_FLAGS) --strict

.PHONY: install run debug clean lint lint-strict
