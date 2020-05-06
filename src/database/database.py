import sqlalchemy
from sqlalchemy.orm import sessionmaker

class Database:
    engine: sqlalchemy.engine
    Session: sessionmaker

    def __init__(self, db_config):
        self.config = db_config
        self.create_engine()

    def create_sql_url(self):
        db_config = self.config
        return "{}://{}:{}@{}:{}/{}".format(db_config["engine"], db_config["username"], db_config["password"],
                                            db_config["server"], db_config["port"], db_config["database"])

    def create_engine(self):
        self.engine = sqlalchemy.create_engine(self.create_sql_url(), echo=True)
        self.Session = sessionmaker(self.engine)
        return

    def query_one_value(self, sql, column):
        with self.engine.connect() as connection:
            result = connection.execute(sql)
            for row in result:
                return row[column]

    def check_and_install(self):
        if self.check_empty_database():
            self.install_database()

    def check_empty_database(self) -> bool:
        return len(self.engine.table_names()) == 0

    def install_database(self):
        pass

    def engine(self):
        return self.engine
