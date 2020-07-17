import cherrypy

from src.views.view import View
from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.models.models import LHead


class ManagementView(View):
    @cherrypy.expose()
    def index(self):
        db_session = Database.Session()
        # TODO: Benutzerabfrage zufügen
        # user = UserManager.get_user(db_session=db_session)
        # if user.is_admin():
        headers = db_session.query(LHead).order_by("order").all()
        template = self.env.get_template('management/character_values.tmpl')
        return template.render(headers=headers)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_get_head(self, head_id=None):
        if head_id is not None:
            # TODO: Benutzerabfrage zufügen
            db_session = Database.Session()
            header: LHead = db_session.query(LHead).filter_by(id=head_id).one()
            return {'id': str(header.id),
                    'title': header.title,
                    'description': header.description,
                    'order': header.order,
                    'standard': header.standard}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def aj_set_head(self, head_id=None, title=None, description=None, order=None, standard=None):
        # TODO: Benutzerabfrage zufügen
        if head_id is not None:
            db_session = Database.Session()
            head: LHead = db_session.query(LHead).filter_by(id=head_id).one()
            head.title = title
            head.description = description
            if standard == "true":
                head.standard = True
            else:
                head.standard = False
            head.order = order
            db_session.commit()
            return {'id': str(head.id),
                    'title': head.title,
                    'description': head.description,
                    'order': head.order,
                    'standard': head.standard}
