import bcrypt
import logging
from unittest.mock import patch
from typing import List

from cherrypy.lib.sessions import RamSession
import pytest
import sqlalchemy.orm


from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.controllers.uuid import UUIDFactory
from src.models.models import User, Character

session: sqlalchemy.orm.Session
fact: UUIDFactory


# Prepare variables
def prepare_variables():
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


def setup_add_user():
    global session
    global fact

    v_user = User(id=fact.create_uuid("user", "Test"),
                  login="Test",
                  username="Test-Benutzer",
                  email="test@test.org",
                  password=bcrypt.hashpw("diesespasswort".encode("utf-8"), bcrypt.gensalt()).decode(),
                  role=0)
    session.add(v_user)
    session.commit()


def setup_create_tables(tables: List[str]):
    queries = {'users': '''CREATE TABLE "users" ("id" uuid PRIMARY KEY, 
                            "login" varchar(50) UNIQUE NOT NULL, 
                            "username" varchar(50) NOT NULL,
                            "email" varchar(255) UNIQUE NOT NULL,
                            "password" varchar(255) NOT NULL,
                            "role" int,
                            "created_at" timestamp);''',
               'characters': '''CREATE TABLE "characters" (
                            "id" uuid PRIMARY KEY,
                            "user_id" uuid NOT NULL,
                            "group_id" uuid,
                            "name" varchar(255));'''}

    prepare_variables()
    setup_clear_database()

    with Database.engine.connect() as connection:
        for key in tables:
            connection.execute(queries[key])
    return


def setup_clear_database():
    with Database.engine.connect() as connection:
        connection.execute("DROP SCHEMA public CASCADE;")
        connection.execute("CREATE SCHEMA public;")
    return


@pytest.fixture()
def fixture_character_empty():
    setup_create_tables(['users', 'characters'])
    setup_add_user()


@pytest.fixture()
def fixture_user_empty():
    setup_create_tables(['users'])


@pytest.fixture()
def fixture_user_data():
    setup_create_tables(['users'])
    setup_add_user()


class TestEmptyDatabase:
    def test_user_save(self, fixture_user_empty):
        global fact
        global session
        test_user = User(id=fact.create_uuid("user", "Test2"),
                         login="Test2",
                         username="test",
                         email="zweiter.test@test.org",
                         password="oderdas",
                         role=0)
        session.add(test_user)
        session.commit()

        assert_user = session.query(User).filter_by(login="Test2").first()
        assert assert_user.email == "zweiter.test@test.org"

    def test_character_save(self, fixture_character_empty):
        global session
        global fact

        sess_mock = RamSession()
        with patch('cherrypy.session', sess_mock, create=True):
            uuid = fact.create_uuid("character", "1234Test Character")
            user_id = UserManager.login('Test', 'diesespasswort')
            user = session.query(User).filter_by(id=user_id).one()
            test_character = Character(id=uuid,
                                       user=user,
                                       name="Test Character")
            session.add(test_character)
            session.commit()

            assert Database.query_one_value("SELECT * FROM \"characters\" WHERE name='Test Character'",
                                            "name") == "Test Character"
            session.commit()


class TestDatabase:
    def test_connect(self, fixture_user_data):
        assert Database.query_one_value("SELECT * FROM \"users\" WHERE login='Test'", "email") == "test@test.org"

    def test_user_read(self, fixture_user_data):
        global session
        assert_user = session.query(User).filter_by(email="test@test.org").one()
        assert assert_user.login == "Test"
