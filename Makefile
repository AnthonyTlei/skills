PYTHON ?= python3

.PHONY: validate install status

validate:
	$(PYTHON) scripts/skills.py validate

install: validate
	$(PYTHON) scripts/skills.py install codex

status:
	$(PYTHON) scripts/skills.py status codex
