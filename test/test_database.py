import pytest
import logging
import bcrypt

from cherrypy.lib.sessions import RamSession
from pytest import *
from unittest.mock import patch
import sqlalchemy.orm

from src.models.models import User, Character
from src.controllers.database_management import Database
from src.controllers.uuid import UUIDFactory
from src.controllers.user_management import UserManager

to_delete = []
session: sqlalchemy.orm.Session
fact: UUIDFactory


@pytest.fixture(scope="class")
def setup_database():
    global to_delete
    global session
    global fact

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
    session = Database.Session()
    fact = UUIDFactory(config={"rootname": "nopnp.org"})
    v_user = User(id=str(fact.create_uuid("user", "Test")),
                  login="Test",
                  username="Test-Benutzer",
                  email="test@test.org",
                  password=bcrypt.hashpw("diesespasswort".encode("utf-8"), bcrypt.gensalt()).decode(),
                  role=0)
    session.add(v_user)
    session.commit()
    to_delete.append(v_user)

    yield
    for row in to_delete:
        session.delete(row)
    session.commit()
    pass


@mark.usefixtures("setup_database")
class TestDatabase:
    def test_connect(self):
        assert Database.query_one_value("SELECT * FROM \"users\" WHERE login='Test'", "email") == "test@test.org"

    def test_user_save(self):
        global fact
        global session
        test_user = User(id=str(fact.create_uuid("user", "Test2")), login="Test2", username="test",
                         email="zweiter.test@test.org", password="oderdas", role=0)
        session.add(test_user)
        session.commit()
        to_delete.append(test_user)

        assert_user = session.query(User).filter_by(login="Test2").first()
        assert assert_user.email == "zweiter.test@test.org"

    def test_user_read(self):
        global session
        assert_user = session.query(User).filter_by(email="test@test.org").one()
        assert assert_user.login == "Test"

    def test_character_save(self):
        global to_delete
        global session
        global fact

        sess_mock = RamSession()
        with patch('cherrypy.session', sess_mock, create=True):
            uuid = str(fact.create_uuid("character", "1234Test Character"))
            user_id = UserManager.login('Test', 'diesespasswort')
            user = session.query(User).filter_by(id=user_id).one()
            test_character = Character(id=uuid,
                                       user=user,
                                       name="Test Character")
            session.add(test_character)
            to_delete.append(test_character)
            session.commit()

            assert Database.query_one_value("SELECT * FROM \"characters\" WHERE name='Test Character'",
                                            "name") == "Test Character"
            session.commit()
