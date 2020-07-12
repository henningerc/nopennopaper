import cherrypy
import json

from src.controllers.character_controller import CharacterController
from src.views.view import View


class AjaxView(View):
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def create_character(self, character_name):
        character = CharacterController.create(character_name)
        return {'id': str(character.id),
                'charactername': character.name}
