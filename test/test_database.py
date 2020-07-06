import bcrypt
import logging
from unittest.mock import patch
from typing import List

from cherrypy.lib.sessions import RamSession
import pytest

from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.controllers.uuid import UUIDFactory
from src.models.models import User, Character, Group, Playerrole, MUserGroup


# Prepare variables
def prepare_variables():
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    config = {
        "server": "localhost",
        "database": "noPnP_test",
        "username": "noPnP",
        "password": "21031208",
        "engine": "postgresql",
        "port": "5432"
    }
    Database(config)


def setup_add_user():
    session = Database.Session()

    v_user = User(id=UUIDFactory.create_uuid("user", "Test"),
                  login="Test",
                  username="Test-Benutzer",
                  email="test@test.org",
                  password=bcrypt.hashpw("diesespasswort".encode("utf-8"), bcrypt.gensalt()).decode(),
                  role=0)
    session.add(v_user)
    session.commit()


def setup_add_group():
    session = Database.Session()
    v_group = Group(name='Testgruppe')
    session.add(v_group)
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
                            "name" varchar(255));''',
               'groups': '''CREATE TABLE "groups" (
                            "id" uuid PRIMARY KEY,
                            "name" varchar(255) NOT NULL);''',
               'm_users_groups': '''CREATE TABLE "m_users_groups" (
                            "id" uuid PRIMARY KEY,
                            "user_id" uuid NOT NULL,
                            "group_id" uuid NOT NULL,
                            "role" playerrole NOT NULL);''',
               'playerrole': '''CREATE TYPE "playerrole" AS ENUM (
                            'spectator',
                            'player',
                            'player_gm',
                            'gm');'''}

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
def fixture_user_group_empty():
    setup_create_tables(['playerrole', 'users', 'groups', 'm_users_groups'])
    setup_add_user()
    setup_add_group()


@pytest.fixture()
def fixture_user_empty():
    setup_create_tables(['users'])


@pytest.fixture()
def fixture_user_data():
    setup_create_tables(['users'])
    setup_add_user()


class TestEmptyDatabase:
    def test_user_save(self, fixture_user_empty):
        session = Database.Session()
        test_user = User(id=UUIDFactory.create_uuid("user", "Test2"),
                         login="Test2",
                         username="test",
                         email="zweiter.test@test.org",
                         password="oderdas",
                         role=0)
        session.add(test_user)
        session.commit()

        assert_user = session.query(User).filter_by(login="Test2").first()
        assert assert_user.email == "zweiter.test@test.org"
        session.commit()

    # TODO: Test does not run through
    def test_character_save(self, fixture_character_empty):
        sess_mock = RamSession()
        with patch('cherrypy.session', sess_mock, create=True):
            session = Database.Session()
            user_id = UserManager.login('Test', 'diesespasswort')
            user = session.query(User).filter_by(id=user_id).one()
            test_character = Character(user=user,
                                       name='Test Character')
            session.add(test_character)
            session.commit()

            assert Database.query_one_value("SELECT * FROM \"characters\" WHERE name='Test Character'",
                                            'name') == 'Test Character'
            session.commit()

    def test_user_group_save(self, fixture_user_group_empty):
        db_session = Database.Session()
        user = db_session.query(User).filter_by(login='Test').one()
        group = db_session.query(Group).filter_by(name='Testgruppe').one()
        user_group = MUserGroup(user=user, group=group, role=Playerrole.gm)
        db_session.add(user_group)
        db_session.commit()
        assert_user = db_session.query(User).filter_by(login='Test').one()
        db_session.commit()
        assert assert_user.groups[0].group.name == 'Testgruppe'
        assert assert_user.groups[0].role != Playerrole.spectator
        assert assert_user.groups[0].role == Playerrole.gm


class TestDatabase:
    def test_connect(self, fixture_user_data):
        assert Database.query_one_value("SELECT * FROM \"users\" WHERE login='Test'", 'email') == 'test@test.org'

    def test_user_read(self, fixture_user_data):
        session = Database.Session()
        assert_user = session.query(User).filter_by(email='test@test.org').one()
        assert assert_user.login == 'Test'
        session.commit()
