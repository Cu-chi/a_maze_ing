PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt
PIP = pip
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
--disallow-untyped-defs --check-untyped-defs
MYPY_STRICT_FLAGS = --strict

install:
	$(PIP) install flake8 mypy

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	@rm -rf __pycache__ .mypy_cache maze.txt

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . $(MYPY_FLAGS)

lint-strict:
	$(PYTHON) -m mypy . $(MYPY_FLAGS) $(MYPY_STRICT_FLAGS)

.PHONY: install run debug clean lint lint-strict
