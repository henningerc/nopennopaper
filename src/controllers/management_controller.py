import cherrypy

from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.models.models import LHead


class ManagementController:
    @staticmethod
    def create_head(db_session, title, description, order, standard):
        head = LHead(title=title, description=description, order=order, standard=standard)
        db_session.add(head)
        db_session.commit()

    @staticmethod
    def create_standard_heads():
        db_session = Database.Session()
        user = UserManager.get_user(True, db_session)
        if user.is_admin():
            ManagementController.create_head(db_session, 'Name', 'Der Name des Characters', 0, True)
            ManagementController.create_head(db_session, 'Familie', 'Die Familie des Characters', 1, True)
            ManagementController.create_head(db_session, 'Geburtstag', 'Der Tag an dem der Character geboren wurde', 2,
                                             True)
        raise cherrypy.HTTPRedirect("/")
