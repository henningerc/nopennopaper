from sqlalchemy import create_engine


class DatabaseException(Exception):
    pass


class DatabaseInstaller:
    engine: object

    def __init__(self, db_config=None):
        self.config = db_config

    def connect(self):
        db_config = self.config
        connection_string = "{}://{}:{}@{}:{}/{}".format(db_config["engine"], db_config["username"],
                                                         db_config["password"], db_config["server"], db_config["port"],
                                                         db_config["database"])
        self.engine = create_engine(connection_string)
        return self.engine
