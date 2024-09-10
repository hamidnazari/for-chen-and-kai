# A simple SQLite3 library with a CLI and HTTP Server

[![Quality Assurance](https://github.com/hamidnazari/for-chen-and-kai/actions/workflows/qa.yml/badge.svg)](https://github.com/hamidnazari/for-chen-and-kai/actions/workflows/qa.yml)

## The Application

```sh
$ ./src/cli.py
usage: cli.py [-h] [-L LOAD] [-l] [-s SEARCH] [-d DELETE] [-i INSERT] [-S] database
cli.py: error: the following arguments are required: database

$ ./src/cli.py data/contacs.db --load data/contacts.csv
$ ./src/cli.py data/contacs.db --list
$ ./src/cli.py data/contacs.db --search Taylor
$ ./src/cli.py data/contacs.db --delete 8196
```

## The Accessories

The following Make targets are here to help:

- `make demo` to see a demo of the projects capabilities
- `make test` to run the tests
- `make run` to build and run a Docker image of the project

For accessing the API endpoinsts, once the container is running:

```bash
$ curl -s http://localhost:8080/info | jq
{
  "git_commit_hash": "e293b06"
}

$ curl http://localhost:8080/list

$ curl http://localhost:8080/search?lastname=Wilson
```
