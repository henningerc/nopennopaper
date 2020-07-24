import cherrypy

from src.views.view import View
from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.controllers.management_controller import ManagementController
from src.models.models import LHead


class ManagementView(View):
    @cherrypy.expose()
    def index(self):
        db_session = Database.Session()
        user = UserManager.get_user(db_session=db_session)
        if user.is_admin():  # TODO: Wenn Benutzer nicht angemeldet Fehlermeldung!
            headers = db_session.query(LHead).order_by("order").all()
            template = self.env.get_template('management/character_values.tmpl')
            return template.render(headers=headers)

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
    def create_heads(self):
        ManagementController.create_standard_heads()

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_delete_head(self, head_id=None):
        if head_id is not None:
            return ManagementController.delete_head(head_id)
