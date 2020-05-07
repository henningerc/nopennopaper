from src.controllers.database_management import Database
from src.models.user import User
import pytest
from pytest import *
import logging
from src.controllers.uuid import UUIDFactory

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
        assert database.query_one_value("SELECT * FROM \"users\" WHERE password='nurmalso'", "login") == "Test"

    def test_user_save(self):
        fact = UUIDFactory(config={"rootname": "nopnp.org"})
        test_user = User(id=str(fact.create_uuid("user", "Test")), login="test", username="test", email="test@test.org",
                         password="erstmaldas", role=0)
        ses = database.Session()
        ses.add(test_user)
        ses.commit()
        assert_user = ses.query(User).filter_by(login="test").first()
        assert assert_user.email == "test@test.org"
        ses.delete(assert_user)
        ses.commit()
        assert_user = ses.query(User).filter_by(login="test").first()
        assert assert_user is None

    def test_user_read(self):
        ses = database.Session()
        assert_user = ses.query(User).filter_by(email="anderertest@test.org").one()
        assert assert_user.password == "nurmalso"
