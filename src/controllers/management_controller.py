import cherrypy

from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.models.models import LHead, LAttribute, LSkill


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
    def set_attribute(db_session, att_id, title, description, short, order, standard):
        attribute: LAttribute = db_session.query(LAttribute).filter_by(id=att_id).one()
        attribute.title = title
        attribute.description = description
        attribute.short = short
        attribute.order = order
        attribute.standard = standard
        db_session.commit()
        return attribute

    @staticmethod
    def create_attribute(db_session, title, description, short, order, standard):
        attribute = LAttribute(title=title, description=description, short=short, order=order, standard=standard)
        db_session.add(attribute)
        db_session.commit()
        return attribute

    @staticmethod
    def create_skill(db_session, title, description, att1, att2, att3, order, standard) -> LSkill:
        attribute1 = db_session.query(LSkill).filter_by(id=att1).one()
        attribute2 = db_session.query(LSkill).filter_by(id=att2).one()
        attribute3 = db_session.query(LSkill).filter_by(id=att3).one()
        skill = LSkill(title=title, description=description, attribute_1=attribute1, attribute_2=attribute2,
                       attribute_3=attribute3, order=order, standard=standard)
        db_session.add(skill)
        db_session.commit()
        return skill

    @staticmethod
    def set_or_create_attribute(db_session, att_id=None, title=None, description=None, short=None, order=None,
                                standard=None) -> LAttribute:
        if att_id == 'new_attribute':
            return ManagementController.create_attribute(db_session, title, description, short, order, standard)
        else:
            return ManagementController.set_attribute(db_session, att_id, title, description, short, order, standard)

    @staticmethod
    def set_skill(db_session, skill_id, title, description, att1, att2, att3, order, standard):
        skill: LSkill = db_session.query(LSkill).filter_by(id=skill_id).one()
        skill.title = title
        skill.description = description
        skill.attribute_1 = db_session.query(LAttribute).filter_by(id=att1).one()
        skill.attribute_2 = db_session.query(LAttribute).filter_by(id=att2).one()
        skill.attribute_3 = db_session.query(LAttribute).filter_by(id=att3).one()
        skill.order = order
        skill.standard = standard
        db_session.commit()
        return skill

    @staticmethod
    def set_or_create_skill(db_session, skill_id=None, title=None, description=None, att1=None, att2=None, att3=None,
                            order=None, standard=None) -> LSkill:
        if skill_id == 'new_skill':
            return ManagementController.create_skill(db_session, title, description, att1, att2, att3, order, standard)
        else:
            return ManagementController.set_skill(db_session, skill_id, title, description, att1, att2, att3, order,
                                                  standard)

    @staticmethod
    def delete_attribute(id):
        db_session = Database.Session()
        user = UserManager.get_user(False, db_session)
        if user is not None and user.is_admin():
            db_session.query(LAttribute).filter_by(id=id).delete()
            db_session.commit()
            return {'id': id, 'deleted': True}
        return {'id': id, 'deleted': False}

    @staticmethod
    def delete_skill(id):
        db_session = Database.Session()
        user = UserManager.get_user(False, db_session)
        if user is not None and user.is_admin():
            db_session.query(LSkill).filter_by(id=id).delete()
            db_session.commit()
            return {'id': id, 'deleted': True}
        return {'id': id, 'deleted': False}
