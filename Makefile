VENV_DIR=.venv
BIN=$(VENV_DIR)/bin
PIP=$(BIN)/pip
PYTHON=$(BIN)/python
POETRY=$(BIN)/poetry

.PHONY: setup venv poetry install lock clean demo

setup: venv poetry install lock

venv:
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@echo "Virtual env created at $(VENV_DIR)"

poetry:
	@$(PIP) install --upgrade pip
	@$(PIP) install poetry
	@$(POETRY) config virtualenvs.in-project true
	@echo "Poetry is ready"

install:
	@$(PIP) install --upgrade pip
	@$(POETRY) install
	@echo "Poetry dependencies installed"

lock:
	@$(POETRY) lock
	@echo "poetry.lock updated"

clean:
	@$(POETRY) env remove python || true
	rm -rf $(VENV_DIR)
	@echo "Cleaned virtual environment"

demo:
	@$(POETRY) run python scripts/man_v_bear_demo.py