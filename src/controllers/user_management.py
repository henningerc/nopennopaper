import bcrypt
import uuid
from src.controllers.database_management import Database
from typing import Union
from src.models.user import User
from src.controllers.uuid import UUIDFactory


class UserManager:
    @staticmethod
    def login(user_login: str, password: str) -> Union[uuid.UUID, None]:
        ses = Database.Session()
        user = ses.query(User).filter_by(login=user_login).first()
        if user is None:
            return None
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return user.id
        else:
            return None

    @staticmethod
    def change_password(user_id: uuid.UUID, password: str):
        ses = Database.Session()
        user = ses.query(User).filter_by(id=str(user_id)).one()
        user.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
        ses.commit()

    @staticmethod
    def create(login=None, username=None, email=None, password=None):
        fact = UUIDFactory
        user = User(id=str(fact.create_uuid("user", login)),
                    login=login,
                    username=username,
                    email=email,
                    password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(),
                    role=1)
        session = Database.Session()
        session.add(user)
        session.commit()

    @staticmethod
    def exists(login=None):
        session = Database.Session()
        ct = session.query(User).filter_by(login=login).count()
        if ct>0:
            return True
        else:
            return False
