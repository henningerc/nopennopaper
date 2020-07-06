from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.models.models import Group, MUserGroup, Playerrole


class GroupManager:
    @staticmethod
    def create(groupname):
        db_session = Database.Session()
        group = Group(name=groupname)
        db_session.add(group)
        user = UserManager.get_user(db_session=db_session)
        user_group = MUserGroup(user=user, group=group, role=Playerrole.gm)
        db_session.add(user_group)
        db_session.commit()
