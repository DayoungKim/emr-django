MOTHER_PYTHON ?= python3.8
VENV_BASE ?= $(PWD)/venv
PYTHON ?= $(VENV_BASE)/bin/python
PIP ?= $(VENV_BASE)/bin/pip

.PHONY: clean venv db

venv:
	if [ "$(VENV_BASE)" ]; then \
		if [ ! -d "$(VENV_BASE)" ]; then \
			virtualenv -p $(MOTHER_PYTHON) $(VENV_BASE); \
			$(PIP) install -r requirements.txt; \
		fi; \
	fi

server:
	$(PYTHON) api/manage.py runserver 0:8000

redis:
	docker-compose -f db-compose.yaml up -d

test: sanity unit

sanity:
	$(VENV_BASE)/bin/flake8 api/*.py
	$(VENV_BASE)/bin/vulture api/*.py --min-confidence 70

unit:
	$(PYTHON) api/manage.py test -v3

clean: clean-venv clean-db clean-file

clean-file:
	#-find . -path "*/migrations/*.pyc"  -delete

clean-venv:
	-rm -rf $(VENV_BASE)
