ifdef PYPI_REPO
  REPO_OPTION=--repository ${PYPI_REPO}
else
	REPO_OPTION=
endif

default: install

install:
	python -m pip install --editable .

lint:
	isort --check --diff . && black --check --diff . && ruff check . && mypy .

publish:
	flit publish $(REPO_OPTION)

test:
	pytest --capture=no --cov=furiosa --cov-report=xml:coverage.xml

doc:
	pdoc3 --html --force --output-dir html_output furiosa

clean:
	rm -rf build dist/* *.egg-info
