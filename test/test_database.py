import bcrypt
import logging
from typing import List

import pytest

from src.controllers.database_management import Database
from src.controllers.uuid import UUIDFactory
from src.models.models import User, Character


# Prepare variables
def prepare_variables() -> None:
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    config = {
        "server": "localhost",
        "database": "noPnP_Test",
        "username": "noPnP_Test",
        "password": "PasswordForTest",
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
               'l_head': '''CREATE TABLE "l_head" (
                            "id" uuid PRIMARY KEY,
                            "title" varchar(255) NOT NULL,
                            "description" text);''',
               'c_head': '''CREATE TABLE "c_head" (
                            "id" uuid PRIMARY KEY,
                            "list_id" uuid NOT NULL,
                            "character_id" uuid NOT NULL,
                            "value_id" uuid NOT NULL);''',
               'v_head': '''CREATE TABLE "v_head" (
                            "id" uuid PRIMARY KEY,
                            "value" varchar(255) NOT NULL,
                            "list_id" uuid NOT NULL);'''}
    
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
def fixture_character_head_empty():
    pass


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

    def test_character_save(self, fixture_character_empty):
        session = Database.Session()

        uuid = UUIDFactory.create_uuid("character", "1234Test Character")
        user = session.query(User).filter_by(login='Test').one()
        test_character = Character(id=uuid,
                                   user=user,
                                   name="Test Character")
        session.add(test_character)
        session.commit()

        assert Database.query_one_value("SELECT * FROM \"characters\" WHERE name='Test Character'",
                                        "name") == "Test Character"

    def test_head_values_save(self):
        pass


class TestDatabase:
    def test_connect(self, fixture_user_data):
        assert Database.query_one_value("SELECT * FROM \"users\" WHERE login='Test'", "email") == "test@test.org"

    def test_user_read(self, fixture_user_data):
        session = Database.Session()
        assert_user = session.query(User).filter_by(email="test@test.org").one()
        assert assert_user.login == "Test"
