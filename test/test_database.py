import pytest
import logging

from cherrypy.lib.sessions import RamSession
from pytest import *
from unittest.mock import patch

from src.models.models import User, Character
from src.controllers.database_management import Database
from src.controllers.uuid import UUIDFactory
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
    def test_connect(self):
        assert Database.query_one_value("SELECT * FROM \"users\" WHERE login='Test'", "email") == "anderertest@test.org"

    def test_user_save(self):
        fact = UUIDFactory(config={"rootname": "nopnp.org"})
        test_user = User(id=str(fact.create_uuid("user", "Test")), login="test", username="test", email="test@test.org",
                         password="erstmaldas", role=0)
        ses = Database.Session()
        ses.add(test_user)
        ses.commit()
        assert_user = ses.query(User).filter_by(login="test").first()
        assert assert_user.email == "test@test.org"
        ses.delete(assert_user)
        ses.commit()
        assert_user = ses.query(User).filter_by(login="test").first()
        assert assert_user is None

    def test_user_read(self):
        ses = Database.Session()
        assert_user = ses.query(User).filter_by(email="anderertest@test.org").one()
        assert assert_user.login == "Test"

    def test_character_save(self):
        fact = UUIDFactory(config={"rootname": "nopnp.org"})
        session = Database.Session()

        sess_mock = RamSession()
        with patch('cherrypy.session', sess_mock, create=True):
            user = UserManager.login('character_test', 'characterpassword')
            test_character = Character(id=str(fact.create_uuid("character", "1234Test Character")),
                                       rel_user=user,
                                       name="Test Character")
            session.add(test_character)
            session.commit()

            assert Database.query_one_value("SELECT * FROM \"characters\" WHERE `name`='Test Character'",
                                            "name") == "Test Character"
        session.delete(test_character)
        session.delete(user)