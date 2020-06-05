from src.controllers.user_management import UserManager


class Installer:
    @staticmethod
    def install():
        if not UserManager.exists('root'):
            UserManager.create(login='root', username='root', email='root@root.lan', password='root')
