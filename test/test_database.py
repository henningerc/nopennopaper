from src.database.database import Database
import pytest
from pytest import *
import logging

database: Database


@pytest.fixture(scope="class")
def setup_database():
    global database

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    config = {
        "server": "localhost",
        "database": "noPnP",
        "username": "postgres",
        "password": "IlFs2000",
        "engine": "postgresql",
        "port": "5432"
    }
    database = Database(config)
    pass


@mark.usefixtures("setup_database")
class TestDatabase:
    def test_connect(self):
        assert database.query_one_value("SELECT * FROM \"Test\"", "Name") == "Test"

    def test_db_empty(self):
        assert database.check_empty_database()

    def test_tables_are_free(self):
        pass
