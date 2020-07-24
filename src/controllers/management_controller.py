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
        return head

    @staticmethod
    def delete_head(id):
        db_session = Database.Session()
        user = UserManager.get_user(False)
        if user is not None and user.is_admin():
            head: LHead = db_session.query(LHead).filter_by(id=id).delete()
            db_session.commit()
            return {'id': id, 'deleted': True}
        return {'id': id, 'deleted': False}

    @staticmethod
    def set_head(db_session, head_id, title, description, order, standard):
        head = db_session.query(LHead).filter_by(id=head_id).one()
        head.title = title
        head.description = description
        if standard == "true":
            head.standard = True
        else:
            head.standard = False
        head.order = order
        db_session.commit()
        return head

    @staticmethod
    def set_or_create_head(db_session, head_id=None, title=None, description=None, order=None, standard=None):
        if head_id == "new":
            return ManagementController.create_head(db_session, title, description, order, standard == 'true')
        else:
            return ManagementController.set_head(db_session, head_id, title, description, order, standard)
