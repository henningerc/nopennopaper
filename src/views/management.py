import cherrypy

from src.views.view import View
from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.controllers.management_controller import ManagementController
from src.models.models import LHead, LAttribute, LSkill


class ManagementView(View):
    @cherrypy.expose()
    def index(self):
        db_session = Database.Session()
        user = UserManager.get_user(db_session=db_session)
        if user.is_admin():
            headers = db_session.query(LHead).order_by('order').all()
            attributes = db_session.query(LAttribute).order_by('order').all()
            skills = db_session.query(LSkill).order_by('order').all()
            template = self.env.get_template('management/character_values.tmpl')
            return template.render(headers=headers, attributes=attributes, skills=skills)

    # AJAX-Calls

    # Attribute

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_get_attribute(self, attribute_id=None):
        if attribute_id is not None:
            db_session = Database.Session()
            user = UserManager.get_user(db_session=db_session)
            if user.is_admin():  # TODO: Wenn Benutzer nicht angemeldet Fehlermeldung!
                attribute: LAttribute = db_session.query(LAttribute).filter_by(id=attribute_id).one()
                return {'id': str(attribute.id),
                        'title': attribute.title,
                        'description': attribute.description,
                        'short': attribute.short,
                        'order': attribute.order,
                        'standard': attribute.standard}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_set_attribute(self, att_id=None, title=None, description=None, short=None, order=None, standard=None):
        if att_id is not None:
            db_session = Database.Session()
            user = UserManager.get_user(db_session=db_session)
            if user.is_admin():  # TODO: Wenn Benutzer nicht angemeldet Fehlermeldung!
                attribute = ManagementController.set_or_create_attribute(db_session, att_id, title, description, short,
                                                                         order, standard == 'true')
                return {'id': str(attribute.id),
                        'title': attribute.title,
                        'description': attribute.description,
                        'short': attribute.short,
                        'order': attribute.order,
                        'standard': attribute.standard}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_delete_attribute(self, att_id=None):
        if att_id is not None:
            return ManagementController.delete_attribute(att_id)

    # Head-Values

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_get_head(self, head_id=None):
        if head_id is not None:
            db_session = Database.Session()
            user = UserManager.get_user(db_session=db_session)
            if user.is_admin():  # TODO: Wenn Benutzer nicht angemeldet Fehlermeldung!
                header: LHead = db_session.query(LHead).filter_by(id=head_id).one()
                return {'id': str(header.id),
                        'title': header.title,
                        'description': header.description,
                        'order': header.order,
                        'standard': header.standard}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_set_head(self, head_id=None, title=None, description=None, order=None, standard=None):
        if head_id is not None:
            db_session = Database.Session()
            user = UserManager.get_user(db_session=db_session)
            if user.is_admin():  # TODO: Wenn Benutzer nicht angemeldet Fehlermeldung!
                head: LHead = ManagementController.set_or_create_head(db_session, head_id, title, description, order,
                                                                      standard)
                return {'id': str(head.id),
                        'title': head.title,
                        'description': head.description,
                        'order': head.order,
                        'standard': head.standard}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_delete_head(self, head_id=None):
        if head_id is not None:
            return ManagementController.delete_head(head_id)

    # Skills

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_get_skill(self, skill_id=None):
        if skill_id is not None:
            db_session = Database.Session()
            user = UserManager.get_user(db_session=db_session)
            if user.is_admin():  # TODO: Wenn Benutzer nicht angemeldet Fehlermeldung!
                skill: LSkill = db_session.query(LSkill).filter_by(id=skill_id).one()
                return {'id': str(skill.id),
                        'title': skill.title,
                        'description': skill.description,
                        'order': skill.order,
                        'standard': skill.standard,
                        'attribute_1': skill.attribute_1_id,
                        'attribute_2': skill.attribute_2_id,
                        'attribute_3': skill.attribute_3_id}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_set_skill(self, skill_id=None, title=None, description=None, attribute_1=None, attribute_2=None,
                     attribute_3=None, order=None, standard=None):
        if skill_id is not None:
            db_session = Database.Session()
            user = UserManager.get_user(db_session=db_session)
            if user.is_admin():  # TODO: Wenn Benutzer nicht angemeldet Fehlermeldung!
                skill: LSkill = ManagementController.set_or_create_skill(db_session, skill_id, title, description,
                                                                         attribute_1, attribute_2, attribute_3, order,
                                                                         standard)
                return {'id': str(skill.id),
                        'title': skill.title,
                        'description': skill.description,
                        'order': skill.order,
                        'standard': skill.standard,
                        'attribute_1': skill.attribute_1_id,
                        'attribute_2': skill.attribute_2_id,
                        'attribute_3': skill.attribute_3_id}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_delete_skill(self, skill_id=None):
        if skill_id is not None:
            return ManagementController.delete_skill(skill_id)
