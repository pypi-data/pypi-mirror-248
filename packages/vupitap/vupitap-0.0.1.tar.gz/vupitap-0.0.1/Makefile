env: venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt --use-pep517
	venv/bin/pip install -e .

venv:
	python3.9 -m venv venv

publish: venv
	rm -fr dist/*
	venv/bin/hatch build
	venv/bin/hatch -v publish

ruff:
	venv/bin/ruff vupitap

mypy:
	venv/bin/mypy vupitap

test:
	venv/bin/pytest $(PYTEST_ME_PLEASE)

check: test ruff mypy
