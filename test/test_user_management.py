import pytest
from src.controllers.database_management import Database
import logging
from pytest import *
from uuid import UUID
from src.controllers.user_management import UserManager


@pytest.fixture(scope="class")
def setup_database():
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
    Database(config)
    pass


@mark.usefixtures("setup_database")
class TestDatabase:
    def test_login(self):
        UserManager.change_password(UUID("021a5206-c359-54df-92e0-f6e764645c64"), "password")
        login = UserManager.login("Test", "password")
        print(login)
        assert login is not None
        UserManager.change_password(UUID("021a5206-c359-54df-92e0-f6e764645c64"), "other_password")
        assert UserManager.login("Test", "password") is None
