import sqlite3
import csv


class Connection:
    def __init__(self, database_name):
        self.database_name = database_name

    def _connect(self):
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def _close(self):
        self.connection.close()

    def _create_table(self, table_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        self.cursor.execute(f"""
            CREATE TABLE {table_name} (
            Identifier INTEGER,
            Lastname TEXT NOT NULL,
            Firstname TEXT NOT NULL,
            Email TEXT
        );""")

    def load(self, csv_filename, table_name="data"):
        self._connect()

        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            self._create_table(table_name)
            for row in reader:
                self.cursor.execute(f"INSERT INTO {table_name} (Identifier, Lastname, Firstname, Email) VALUES (?, ?, ?, ?)", row)

        self.connection.commit()
        self._close()
