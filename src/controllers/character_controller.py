from typing import Optional

from src.models.models import Character, LHead, CHead, LAttribute, CAttribute, LSkill, CSkill
from src.controllers.database_management import Database
from src.controllers.user_management import UserManager


class CharacterController:
    @staticmethod
    def create(charactername, db_session=None) -> Optional[Character]:
        if charactername == "":
            return None
        if db_session is None:
            db_session = Database.Session()
        user = UserManager.get_user(db_session=db_session)
        character = Character(user=user, name=charactername)
        db_session.add(character)

        heads = db_session.query(LHead).filter_by(standard=True).all()
        for h in heads:
            c_h = CHead(character=character, list=h, value_id=None)
            db_session.add(c_h)

        attributes = db_session.query(LAttribute).filter_by(standard=True).all()
        for a in attributes:
            c_a = CAttribute(character=character, list=a, value=0)
            db_session.add(c_a)

        skills = db_session.query(LSkill).filter_by(standard=True).all()
        for s in skills:
            c_s = CSkill(character=character, list=s)
            db_session.add(c_s)

        db_session.commit()
        return character
