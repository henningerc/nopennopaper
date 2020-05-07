import bcrypt
import uuid
from src.controllers.database_management import Database
from typing import Union
from src.models.user import User


class UserManager:
    @staticmethod
    def login(user_login: str, password: str) -> Union[uuid.UUID, None]:
        ses = Database.Session()
        user = ses.query(User).filter_by(login=user_login).one()
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
