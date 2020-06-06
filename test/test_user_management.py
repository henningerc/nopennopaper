import pytest
import logging
import cherrypy

from cherrypy.lib.sessions import RamSession
from pytest import *
from unittest.mock import patch
from uuid import UUID

from src.controllers.database_management import Database
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
class TestUserManagement:
    def test_login(self):
        UserManager.change_password(UUID("021a5206-c359-54df-92e0-f6e764645c64"), "password")
        sess_mock = RamSession()
        with patch('cherrypy.session', sess_mock, create=True):
            login = UserManager.login("Test", "password")
            print(login)
            assert login is not None
            UserManager.change_password(UUID("021a5206-c359-54df-92e0-f6e764645c64"), "other_password")
            assert UserManager.login("Test", "password") is None

    def test_create_user(self):
        UserManager.create('test2', 'test2', 'test@test.tdl', 'test_password')
        sess_mock = RamSession()
        with patch('cherrypy.session', sess_mock, create=True):
            login = UserManager.login('test2', 'test_password')
            assert login is not None
            UserManager.delete(login)
            login = UserManager.login('test2', 'test_password')
            assert login is None

