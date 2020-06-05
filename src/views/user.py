import cherrypy
from src.views.view import View
from src.controllers.user_management import UserManager


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
