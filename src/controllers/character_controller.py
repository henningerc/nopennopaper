from src.models.models import Character
from src.controllers.database_management import Database
from src.controllers.user_management import UserManager


class CharacterController:
    @staticmethod
    def create(charactername, db_session=None) -> Character:
        if db_session is None:
            db_session = Database.Session()
        user = UserManager.get_user(db_session=db_session)
        character = Character(user=user, name=charactername)
        db_session.add(character)
        db_session.commit()
        return character
