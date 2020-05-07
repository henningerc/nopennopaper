import cherrypy
from src.views.view import View


class UserView(View):
    @cherrypy.expose
    def login(self):
        template = self.env.get_template("/users/login.tmpl")
        output = template.render()
        return output
