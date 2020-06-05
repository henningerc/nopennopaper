import sqlalchemy
from sqlalchemy.orm import sessionmaker
from typing import Union


class Database:
    engine: sqlalchemy.engine
    Session: sessionmaker

    def __init__(self, db_config):
        Database.config = db_config
        Database.create_engine()

    @staticmethod
    def create_engine():
        Database.engine = sqlalchemy.create_engine(Database.create_sql_url(), echo=True)
        Database.Session = sessionmaker(Database.engine)
        return

    @staticmethod
    def create_sql_url() -> str:
        db_config = Database.config
        return "{}://{}:{}@{}:{}/{}".format(db_config["engine"], db_config["username"], db_config["password"],
                                            db_config["server"], db_config["port"], db_config["database"])

    @staticmethod
    def query_one_value(sql: str, column: str) -> Union[int, str]:
        with Database.engine.connect() as connection:
            result = connection.execute(sql)
            for row in result:
                return row[column]
