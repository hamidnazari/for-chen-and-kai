DB_FILENAME:=contacts.db
CSV_FILENAME:=contacts.csv

define echo_info
	@echo "\033[33m$(1)\033[0m"
endef

venv:
	@python3 -m venv ./venv
	@source ./venv/bin/activate

deps: venv
	@pip3 install -Ur requirements.txt

test: deps
	@python3 -m pytest

lint: deps
	@pylint src/

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
	$(call echo_info,Launching API server.)
	python3 src/cli.py $(DB_FILENAME) --server &
	sleep 2

	@echo
	$(call echo_info,Searching for lastname Doe via the API.)
	curl "http://localhost:8080/search?lastname=Doe"

	@echo
	@echo
	$(call echo_info,Terminating this and all subprocesses.)
	@trap 'kill 0' EXIT;

.PHONE: venv deps test lint demo
