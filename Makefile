PROJECT = aiohug

PYTHON_VERSION = 3.6
REQUIREMENTS = requirements.txt
REQUIREMENTS_TEST = requirements-test.txt
VIRTUAL_ENV ?= .venv
PYTHON ?= $(VIRTUAL_ENV)/bin/python
PIP_CONF = pip.conf
PYPI = pypi


pip_install:
	pip install -r requirements-test.txt

ci_test:
	pytest --flake8 --cov-report html:.reports/coverage --cov-config .coveragerc --cov $(PROJECT)

ci_coveralls:
	GIT_ID="$(CI_COMMIT_SHORT_SHA)" GIT_BRANCH="$(CI_COMMIT_REF_NAME)" COVERALLS_PARALLEL=true coveralls

test: venv
	$(VIRTUAL_ENV)/bin/py.test

test_coverage: venv
	$(VIRTUAL_ENV)/bin/py.test --cov-report html:.reports/coverage --cov-config .coveragerc --cov $(PROJECT)

venv_init:
	pip install virtualenv
	if [ ! -d $(VIRTUAL_ENV) ]; then \
		virtualenv -p python$(PYTHON_VERSION) --prompt="($(PROJECT)) " $(VIRTUAL_ENV); \
	fi

venv:  venv_init
	$(VIRTUAL_ENV)/bin/pip install -r $(REQUIREMENTS_TEST)

clean_venv:
	rm -rf $(VIRTUAL_ENV)

clean_pyc:
	find . -name \*.pyc -delete

clean: clean_venv clean_pyc

