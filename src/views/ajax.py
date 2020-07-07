import cherrypy
import json


from src.views.view import View


class AjaxView(View):
    @cherrypy.expose()
    def submit(self, value):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        text = json.dumps(dict(value=value))
        return text.encode('utf-8')
