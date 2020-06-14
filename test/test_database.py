import bcrypt
import logging
from typing import List

import pytest

from src.controllers.database_management import Database
from src.models.models import User, Character, LHead, VHead, CHead


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

    v_user = User(login="Test",
                  username="Test-Benutzer",
                  email="test@test.org",
                  password=bcrypt.hashpw("diesespasswort".encode("utf-8"), bcrypt.gensalt()).decode(),
                  role=0)
    session.add(v_user)
    session.commit()
    return v_user


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


def setup_add_head_list():
    session = Database.Session()
    head_list = LHead(title='Test Liste', description='Test Description')
    session.add(head_list)
    session.commit()
    return head_list


def setup_add_head_value(head_list: LHead):
    session = Database.Session()
    head_value = VHead(value='Test Wert', list=head_list)
    session.add(head_value)
    session.commit()
    return head_value


def setup_add_character(v_user: User):
    session = Database.Session()
    v_character = Character(user=v_user, name='Testcharacter')
    session.add(v_character)
    session.commit()
    return v_character


@pytest.fixture()
def fixture_character_empty():
    setup_create_tables(['users', 'characters'])
    setup_add_user()


@pytest.fixture()
def fixture_character_head_empty():
    setup_create_tables(['users', 'characters', 'c_head', 'l_head', 'v_head'])
    v_user = setup_add_user()
    setup_add_character(v_user)
    head_list = setup_add_head_list()
    setup_add_head_value(head_list)
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
        test_user = User(login="Test2",
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

        user = session.query(User).filter_by(login='Test').one()
        test_character = Character(user=user,
                                   name="Test Character")
        session.add(test_character)
        session.commit()

        assert Database.query_one_value("SELECT * FROM \"characters\" WHERE name='Test Character'",
                                        "name") == "Test Character"
        character = session.query(Character).filter_by(name='Test Character').one()
        assert character.user.email == 'test@test.org'

    def test_head_values_save(self, fixture_character_head_empty):
        head_list: LHead
        session = Database.Session()
        character = session.query(Character).filter_by(name='Testcharakter').first()
        head_list = session.query(LHead).filter_by(title='Test Liste').first()
        head_value = head_list.values[0]
        head_connection = CHead(list=head_list, value=head_value, character=character)
        session.add(head_connection)
        session.commit()

        check_character = session.query(Character).filter_by(name='Testcharakter').first()
        assert check_character.head_values[0].list.title == 'Test Liste'
        pass


class TestDatabase:
    def test_connect(self, fixture_user_data):
        assert Database.query_one_value("SELECT * FROM \"users\" WHERE login='Test'", "email") == "test@test.org"

    def test_user_read(self, fixture_user_data):
        session = Database.Session()
        assert_user = session.query(User).filter_by(email="test@test.org").one()
        assert assert_user.login == "Test"
