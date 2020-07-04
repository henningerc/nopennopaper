import cherrypy
from src.views.view import View
from src.models.models import Character, User
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

    @cherrypy.expose
    def create(self, charactername=None, button=None):
        if button is None:
            user = UserManager.get_user()
            template = self.env.get_template("/character/create.tmpl")
            return template.render(user=user)
        if charactername is not None and charactername != "":
            session = Database.Session()
            user = UserManager.get_user(db_session=session)
            character = Character(user=user, name=charactername)
            session.add(character)
            session.commit()
        raise cherrypy.HTTPRedirect("/character/view?id=" + str(character.id))
