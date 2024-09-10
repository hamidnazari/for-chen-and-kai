DB_FILENAME:=data/contacts.db
CSV_FILENAME:=data/contacts.csv

export GIT_COMMIT_HASH=$(shell git rev-parse --short HEAD)

define echo_info
	@echo "\033[33m$(1)\033[0m"
endef

venv:
	@python3 -m venv ./venv

deps: venv
	@bash ./venv/bin/activate
	@pip3 install -Ur requirements.txt

test: deps
	@python3 -m pytest

lint: deps
	@pylint src/

image:
	@docker compose build

run:
	@docker compose up -d --build

stop:
	@docker compose down

demo: deps
	$(call echo_info,Demonstrating capabilities of the SQLite3 CLI.)
	$(call echo_info,Loading the contents of ${CSV_FILENAME} into SQLite3 database: ${DB_FILENAME})
	python3 src/cli.py $(DB_FILENAME) --load $(CSV_FILENAME)

	@echo
	$(call echo_info,Displaying the first 5 records in the database. Notice Davis.)
	python3 src/cli.py $(DB_FILENAME) --list | head -n 5

	@echo
	$(call echo_info,Deleting record with Identifier 3786.)
	python3 src/cli.py $(DB_FILENAME) --delete 3786

	@echo
	$(call echo_info,Displaying the first 5 records in the database again. Notice Davis.)
	python3 src/cli.py $(DB_FILENAME) --list | head -n 5

	@echo
	$(call echo_info,Inserting a new record for John Doe.)
	python3 src/cli.py $(DB_FILENAME) --insert '9999,Doe,John,john.doe@example.com'

	@echo
	$(call echo_info,Searching for records with lastname Doe.)
	python3 src/cli.py $(DB_FILENAME) --search Doe

	@echo
	$(call echo_info,Launching API server Docker container.)
	@make run
	@sleep 3

	@echo
	$(call echo_info,Looking up server /info endpoint.)
	curl "http://localhost:8080/info"

	@echo
	$(call echo_info,Searching for lastname Doe via the API.)
	curl "http://localhost:8080/search?lastname=Doe"

	@echo
	@echo
	$(call echo_info,Stopping all Docker services.)
	@make stop

.PHONE: venv deps test lint demo image run stop
