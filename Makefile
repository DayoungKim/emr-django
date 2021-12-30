PY_VERSION ?= 3.8.7
PY_ENV := $(if $($(PYTHON)3 --version | grep $(PY_VERSION)), $(PYTHON)3, $(PYENV_ROOT)/versions/$(PY_VERSION)/bin/python)
VENV_BASE ?= $(PWD)/venv
PYTHON ?= $(VENV_BASE)/bin/python
PIP ?= $(VENV_BASE)/bin/pip

.PHONY: clean venv db

venv:
	if [ "$(VENV_BASE)" ]; then \
		if [ ! -d "$(VENV_BASE)" ]; then \
			virtualenv -p $(PY_ENV) $(VENV_BASE); \
			$(PIP) install -r requirements.txt; \
		fi; \
	fi

server:
	$(PYTHON) api/manage.py runserver 0:8000

test: sanity unit

sanity:
	$(VENV_BASE)/bin/flake8
	$(VENV_BASE)/bin/vulture *.py --min-confidence 70

unit:
	$(PYTHON) api/manage.py test -v3

clean: clean-venv clean-db clean-file

clean-file:
	#-find . -path "*/migrations/*.pyc"  -delete

clean-venv:
	-rm -rf $(VENV_BASE)
