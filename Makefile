VENV_DIR=.venv
PYTHON=python3

UNAME_S := $(shell uname -s)

ifeq ($(OS),Windows_NT)
    PIP=$(VENV_DIR)/Scripts/pip.exe
else ifeq ($(UNAME_S),Darwin)
    PIP=$(VENV_DIR)/bin/pip
else ifeq ($(UNAME_S),Linux)
    PIP=$(VENV_DIR)/bin/pip
else
    PIP=$(VENV_DIR)/bin/pip
endif

.PHONY: venv

venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment in $(VENV_DIR)"; \
		$(PYTHON) -m venv $(VENV_DIR); \
		"$(PIP)" install --upgrade pip; \
	else \
		echo "Virtualenv already exists in $(VENV_DIR)"; \
	fi
