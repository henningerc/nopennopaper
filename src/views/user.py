import cherrypy
from src.views.view import View
from src.controllers.user_management import UserManager
from src.models.models import User
from src.controllers.database_management import Database


class UserView(View):
    @cherrypy.expose
    def login(self, user=None, password=None):
        if user is None or password is None:
            template = self.env.get_template("/user/login.tmpl")
            return template.render()
        else:
            if UserManager.login(user, password) is not None:
                raise cherrypy.HTTPRedirect("/user")
            else:
                return "Fehler!"

    @cherrypy.expose
    def index(self):
        user = UserManager.get_user()
        template = self.env.get_template("/user/index.tmpl")
        return template.render(user=user)

