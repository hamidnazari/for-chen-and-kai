DB_FILENAME:=contacts.db
CSV_FILENAME:=contacts.csv


venv:
	@python3 -m venv ./venv

deps:
	@pip3 install -r requirements.txt

test: deps
	@python3 -m pytest

lint: deps
	@pylint src/

example: deps
	@echo "Demonstrating capabilities of the SQLite3 CLI."
	@echo "Loading the contents of ${CSV_FILENAME} into SQLite3 database: ${DB_FILENAME}"
	python3 src/cli.py $(DB_FILENAME) --load $(CSV_FILENAME)

.PHONE: venv deps test lint example
