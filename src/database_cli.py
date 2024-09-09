import argparse
from db.connection import Connection


class DatabaseCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="SQLite Database CLI")
        self.parser.add_argument("database", help="SQLite database file name")
        self.parser.add_argument("-l", "--load", help="Load CSV dataset into the database")
        self.parser.add_argument("-s", "--search", help="Lookup a record by value")
        self.parser.add_argument("-d", "--delete", help="Delete a record by identifier")
        self.parser.add_argument("-i", "--insert", nargs=2, metavar=("TABLE", "VALUES"),
                                 help= "Insert a new entry by passing a comma-separated list of values")
        self.args = self.parser.parse_args()

    def run(self):
        connection = Connection(self.args.database)

        if self.args.load:
            connection.load(self.args.load)
            pass
        elif self.args.list:
            pass
        elif self.args.search:
            pass
        elif self.args.delete:
            pass
        elif self.args.insert:
            pass
        else:
            self.parser.print_help()

