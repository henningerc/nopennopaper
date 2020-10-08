import cherrypy
from typing import Optional

from src.views.view import View
from src.models.models import Character, CHead, VHead
from src.controllers.user_management import UserManager
from src.controllers.database_management import Database
from src.controllers.character_controller import CharacterController


class CharacterView(View):
    @cherrypy.expose
    def index(self):
        pass

    # TODO: Tests for the view
    @cherrypy.expose
    def view(self, id):
        session = Database.Session()
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
            character = CharacterController.create(charactername)
        raise cherrypy.HTTPRedirect("/character/view?id=" + str(character.id))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def aj_get_character_head(self, aj_id):
        head: Optional[CHead] = CharacterController.get_head(aj_id)
        return {
            'id': str(head.id),
            'title': head.list.title,
            'lhead_id': str(head.list_id)
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def aj_get_vhead_list(self, lhead):
        db_session = Database.Session()
        vhead_list = []
        vheads = db_session.query(VHead).order_by('value').filter_by(list_id=lhead).all()
        for val in vheads:
            vhead_list.append({'id': str(val.id), 'text': val.value})
        return vhead_list
