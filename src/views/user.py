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
                raise cherrypy.HTTPRedirect("/")
            else:
                return "Fehler!"

    @cherrypy.expose
    def index(self):
        user = UserManager.get_user()
        template = self.env.get_template("user/show.tmpl")
        return template.render(user=user)

    @cherrypy.expose()
    def list(self):
        session = Database.Session()
        user = UserManager.get_user(db_session=session)
        if user.is_admin():
            users = session.query(User).all()
            template = self.env.get_template("user/list.tmpl")
            return template.render(users=users)
        else:
            template = self.env.get_template("errors/admin.tmpl")
            return template.render()

    @cherrypy.expose()
    def show(self, user_id=None):
        if user_id is None:
            return self.index()
        else:
            user = UserManager.get_user()
            if user.is_admin or str(user.id) == user_id:
                db_ses = Database.Session()
                user = db_ses.query(User).filter_by(id=user_id).first()
                template = self.env.get_template('/user/show.tmpl')
                return template.render(user=user)
            else:
                template = self.env.get_template('errors/admin.tmpl')
                return template.render()

    @cherrypy.expose()
    def create(self, username=None, login=None, password=None, email=None, submit=None):
        user = UserManager.get_user()
        if user.is_admin():
            if submit is None:
                template = self.env.get_template('user/create.tmpl')
                return template.render()
            else:
                user = UserManager.create(login, username, email, password)
                raise cherrypy.HTTPRedirect("/user/show?user_id=" + str(user.id))
        else:
            template = self.env.get_template('errors/admin.tmpl')
            return template.render()
