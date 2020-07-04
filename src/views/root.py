import cherrypy

from src.views.view import View
from src.views.user import UserView
from src.views.character import CharacterView


class RootView(View):
    def __init__(self):
        self.user = UserView()
        self.character = CharacterView()

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/user/login")

