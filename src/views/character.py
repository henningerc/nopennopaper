import cherrypy
from src.views.view import View
from src.models.models import Character
from src.controllers.user_management import UserManager
from src.controllers.database_management import Database


class CharacterView(View):
    @cherrypy.expose
    def index(self):
        pass

    # TODO: Tests for the view
    @cherrypy.expose
    def view(self, id):
        session = Database.Session
        character = session.query(Character).filter_by(id=id).one()
        if UserManager.able_view_character(character):
            template = self.env.get_template('/character/view.tmpl')
            return template.render(character=character)
        pass
