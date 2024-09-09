import sqlite3
import csv
import sys

class Connection:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = None
        self.cursor = None

    def _connect(self):
        try:
            self.connection = sqlite3.connect(self.database_name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error connecting to SQLite database: {e}")

    def _close(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error closing SQLite database connection: {e}")

    def _create_table(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            self.cursor.execute(f"""
                CREATE TABLE {table_name} (
                Identifier INTEGER,
                Lastname TEXT NOT NULL,
                Firstname TEXT NOT NULL,
                Email TEXT);
            """)
        except sqlite3.Error as e:
            sys.stderr.write(f"Error creating table: {e}")

    def load(self, csv_filename, table_name="data"):
        self._connect()

        try:
            with open(csv_filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                self._create_table(table_name)
                for row in reader:
                    self.cursor.execute(f"""
                        INSERT INTO {table_name} (Identifier, Lastname, Firstname, Email)
                        VALUES (?, ?, ?, ?);
                    """, row)

            self.connection.commit()
        except FileNotFoundError:
            sys.stderr.write(f"File not found: {csv_filename}")
        except csv.Error as e:
            sys.stderr.write(f"Error reading CSV file: {e}")
        except sqlite3.Error as e:
            sys.stderr.write(f"Error inserting data into SQLite database: {e}")

        self._close()

    def list(self, table_name="data"):
        result = None
        self._connect()

        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            result = self.cursor.fetchall()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error fetching data from SQLite database: {e}")

        self._close()

        return result

    def search(self, lastname, table_name="data"):
        result = None
        self._connect()

        try:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE Lastname = ?", (lastname,))
            result = self.cursor.fetchall()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error searching SQLite database: {e}")

        self._close()

        return result

    def delete(self, identifier, table_name="data") -> bool:
        self._connect()

        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE Identifier = ?", (identifier,))
            self.connection.commit()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error deleting from SQLite database: {e}")
            return False

        self._close()
        return True
