import os

from jinja2 import Environment, FileSystemLoader
import cherrypy

from src.views.view import View
from src.views.user import UserView
from src.views.character import CharacterView
from src.views.group import GroupView


class RootView(View):
    def __init__(self):
        self.file_loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
        self.env = Environment(loader=self.file_loader)

        self.user = UserView()
        self.character = CharacterView()
        self.group = GroupView()

    @cherrypy.expose
    def index(self):
        template = self.env.get_template('root/index.tmpl')
        return template.render()


