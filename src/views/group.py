import cherrypy

from src.views.view import View
from src.controllers.user_management import UserManager
from src.controllers.group_management import GroupManager


class GroupView(View):
    @cherrypy.expose()
    def create(self, groupname=None, submit=None):
        UserManager.get_user()
        if submit is None:
            template = self.env.get_template('group/create.tmpl')
            return template.render()
        else:
            if groupname is not None:
                GroupManager.create(groupname)
            raise cherrypy.HTTPRedirect("/")
