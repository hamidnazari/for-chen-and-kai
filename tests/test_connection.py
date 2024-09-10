import os
import pytest
from src.db.connection import Connection


@pytest.fixture
def db_connection():
    test_db = 'test_database.db'
    conn = Connection(test_db)
    yield conn


def test_load_csv(db_connection):
    test_csv = 'data/contacts.csv'
    db_connection.load(test_csv)

    result = db_connection.list()

    assert len(result) == 10_000
