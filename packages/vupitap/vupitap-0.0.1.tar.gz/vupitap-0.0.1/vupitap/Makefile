ruff:
	../venv/bin/flake8 .

mypy:
	../venv/bin/mypy .

test:
	../venv/bin/pytest $(PYTEST_ME_PLEASE)

check: test ruff mypy
