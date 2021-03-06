import os
import sys

import configparser
import cherrypy

from src.views.root import RootView
from src.controllers.database_management import Database
from src.controllers.install_controller import InstallController


class NoPnP:
    install: bool = False
    install_heads: bool = False
    install_attributes: bool = False
    install_skills: bool = False

    def __init__(self, arguments=None):
        configfile = 'nopnp.conf'

        if arguments is not None:
            status = 'n'
            for arg in arguments:
                if status == 'n':
                    if arg == '-c':
                        status = 'c'
                    elif arg == '--install':
                        self.install = True
                    elif arg == '--install_heads':
                        self.install_heads = True
                    elif arg == '--install_attributes':
                        self.install_attributes = True
                    elif arg == '--install_skills':
                        self.install_skills = True
                elif status == 'c':
                    configfile = arg
                    status = 'n'

        self.config = self.load_config(configfile)

    @staticmethod
    def load_config(filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def startup(self):
        Database(self.config['Database'])
        if self.install:
            InstallController.install()
        else:
            if self.install_heads:
                InstallController.create_standard_heads()
            if self.install_attributes:
                InstallController.create_standard_attributes()
            if self.install_skills:
                InstallController.create_standard_skills()

        conf = {
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views', 'static')
            }
        }
        cherrypy.config.update({
            'server.socket_port': int(self.config['HTTP']['port']),
            'tools.sessions.on': True,
        })
        cherrypy.tree.mount(RootView(), '/', config=conf)
        cherrypy.engine.start()
        cherrypy.engine.block()


application = NoPnP(sys.argv)
application.startup()
