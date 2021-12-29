PY_VERSION ?= 3.8.7
PY_ENV := $(if $($(PYTHON)3 --version | grep $(PY_VERSION)), $(PYTHON)3, $(PYENV_ROOT)/versions/$(PY_VERSION)/bin/python)
VENV_BASE ?= $(PWD)/venv
PYTHON ?= $(VENV_BASE)/bin/python
PIP ?= $(VENV_BASE)/bin/pip
DB_BASE ?= $(PWD)/db
DB_DUMP_FILE ?= $(PWD)/staging.sql
DB_ENDPOINT ?= 
$(shell aws rds describe-db-instances --db-instance-identifier staging | jq '.DBInstances[] | .Endpoint | .Address')

.PHONY: clean venv db

venv:
	if [ "$(VENV_BASE)" ]; then \
		if [ ! -d "$(VENV_BASE)" ]; then \
			virtualenv -p $(PY_ENV) $(VENV_BASE); \
			$(PIP) install -r requirements.txt; \
		fi; \
	fi

db-file:
	-rm -rf $(DB_DUMP_FILE)
	pg_dump -Fc -v -h $(DB_ENDPOINT) -U meraki meraki_staging > $(DB_DUMP_FILE);

db-container:
	if [ "$(DB_BASE)" ]; then \
		if [ ! -d "$(DB_BASE)" ]; then \
			mkdir $(DB_BASE); \
		fi; \
	fi
	docker-compose -f db-compose.yaml up -d
	@echo "wait db to start up..."
	sleep 20
	-pg_restore -v -W -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) $(DB_DUMP_FILE)

server:
	if [ ! -f "$(FIREBASE_CREDENTIAL)" ]; then \
		aws s3 cp s3://mydoctor-server/credentials/mydoctor-firebase.json $(FIREBASE_CREDENTIAL); \
	fi
	$(PYTHON) manage.py runserver 0:8000

beat:
	$(VENV_BASE)/bin/celery -A conf beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler

worker:
	$(VENV_BASE)/bin/celery -A conf worker --loglevel=debug

img:
	docker build -t mydoc:latest .
	docker save -o mydoc.img mydoc:latest

all-service:
	if [ "$(DB_BASE)" ]; then \
		if [ ! -d "$(DB_BASE)" ]; then \
			mkdir $(DB_BASE); \
		fi; \
	fi
	docker-compose up -d

test: sanity unit

sanity:
	$(VENV_BASE)/bin/flake8
	$(VENV_BASE)/bin/vulture *.py --min-confidence 70

unit:
	$(PYTHON) manage.py test -v3

clean: clean-venv clean-db clean-file

clean-file:
	#-find . -path "*/migrations/*.pyc"  -delete
	-rm -rf $(FIREBASE_CREDENTIAL)
	-rm -rf server.log
	-rm -rf gunicorn.access.log
	-rm -rf gunicorn.error.log

clean-venv:
	-rm -rf $(VENV_BASE)

clean-db-file:
	-rm -rf $(DB_DUMP_FILE)

clean-db-container:
	-docker-compose down
	-rm -rf $(DB_BASE)

clean-db: clean-db-container clean-db-file

new-db: clean-db db-file db-container

db: clean-db-container db-container
