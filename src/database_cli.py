import os
import sys
import argparse

import server
from db.connection import Connection

class DatabaseCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="SQLite Database CLI.")
        self.parser.add_argument("database", help="SQLite database file name")
        self.parser.add_argument("-L", "--load", help="Load CSV dataset into the database")
        self.parser.add_argument("-l", "--list", action="store_true",
                                 help="List the data stored in the database")
        self.parser.add_argument("-s", "--search", help="Lookup a record by value")
        self.parser.add_argument("-d", "--delete", help="Delete a record by identifier")
        self.parser.add_argument("-i", "--insert",
                                 help= "Insert a comma-separated list of values into the database")
        self.parser.add_argument("-S", "--server", action="store_true",
                                 help="Serve an API with /list and /search?lastname= endpoints")
        self.args = self.parser.parse_args()

    def _print_results(self, results):
        for result in results:
            try:
                sys.stdout.write(", ".join(str(i) for i in result))
                sys.stdout.write("\n")
                sys.stdout.flush()
            except BrokenPipeError:
                with open(os.devnull, 'w', encoding="utf-8") as devnull:
                    sys.stdout = devnull
                break

    def run(self) -> int:
        connection = Connection(self.args.database)

        if self.args.load:
            try:
                connection.load(self.args.load)
            # pylint: disable=broad-except
            except Exception as e:
                sys.stderr.write(f"Could not load dataset: {e}")
                return 1

            return 0

        elif self.args.list:
            results = connection.list()
            self._print_results(results)

        elif self.args.search:
            results = connection.search(self.args.search)
            self._print_results(results)

        elif self.args.delete:
            results = connection.delete(self.args.delete)

            if results:
                sys.stdout.write(f"Deleted record with id: {self.args.delete}")
                sys.stdout.write("\n")
                return 0
            else:
                sys.stderr.write(f"Could not delete record with id: {self.args.delete}")
                sys.stderr.write("\n")
                return 1

        elif self.args.insert:
            values = self.args.insert.split(',')
            results = connection.insert(values)

            if results:
                sys.stdout.write(f"Inserted record with values: {values}")
                sys.stdout.write("\n")
                return 0
            else:
                sys.stderr.write(f"Could not insert record with values: {values}")
                sys.stderr.write("\n")
                return 1

        elif self.args.server:
            server.run(connection)

        else:
            self.parser.print_help()
            return 1

