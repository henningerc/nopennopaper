import cherrypy

from src.controllers.database_management import Database
from src.controllers.user_management import UserManager
from src.views.view import View
from src.views.user import UserView
from src.views.character import CharacterView
from src.views.group import GroupView
from src.views.ajax import AjaxView


class RootView(View):
    def __init__(self):
        super().__init__()
        self.user = UserView()
        self.character = CharacterView()
        self.group = GroupView()
        self.ajax = AjaxView()

    @cherrypy.expose
    def index(self):
        session = Database.Session()
        user = UserManager.get_user(required=False, db_session=session)
        template = self.env.get_template('root/index.tmpl')
        return template.render(user=user)


