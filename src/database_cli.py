import argparse
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
        self.parser.add_argument("-i", "--insert", nargs=2, metavar=("TABLE", "VALUES"),
                                 help= "Insert a comma-separated list of values into the database")
        self.args = self.parser.parse_args()

    def _print_results(self, results):
        for result in results:
            print(", ".join(str(i) for i in result))

    def run(self):
        connection = Connection(self.args.database)

        if self.args.load:
            connection.load(self.args.load)
        elif self.args.list:
            results = connection.list()
            self._print_results(results)
        elif self.args.search:
            results = connection.search(self.args.search)
            self._print_results(results)
        elif self.args.delete:
            results = connection.delete(self.args.delete)
            print(f"Deleted record with id: {self.args.delete}" \
                  if results else \
                "Could not delete record with id: {self.args.delete}")
        elif self.args.insert:
            pass
        else:
            self.parser.print_help()
