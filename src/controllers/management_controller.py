import cherrypy

from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.models.models import LHead, LAttribute


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

    @staticmethod
    def set_attribute(db_session, att_id, title, description):
        attribute: LAttribute = db_session.query(LAttribute).filter_by(id=att_id).one()
        attribute.title = title
        attribute.description = description
        db_session.commit()
        return attribute

    @staticmethod
    def create_attribute(db_session, title, description):
        attribute = LAttribute(title=title, description=description)
        db_session.add(attribute)
        db_session.commit()
        return attribute

    @staticmethod
    def set_or_create_attribute(db_session, att_id=None, title=None, description=None) -> LAttribute:
        if att_id == 'new_attribute':
            return ManagementController.create_attribute(db_session, title, description)
        else:
            return ManagementController.set_attribute(db_session, att_id, title, description)

    @staticmethod
    def delete_attribute(id):
        db_session = Database.Session()
        user = UserManager.get_user(False, db_session)
        if user is not None and user.is_admin():
            db_session.query(LAttribute).filter_by(id=id).delete()
            db_session.commit()
            return {'id': id, 'deleted': True}
        return {'id': id, 'deleted': False}
