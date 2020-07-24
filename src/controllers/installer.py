from src.controllers.user_management import UserManager
from src.controllers.management_controller import ManagementController
from src.controllers.database_management import Database


class Installer:
    @staticmethod
    def install():
        if not UserManager.exists('root'):
            UserManager.create(login='root', username='root', email='root@root.lan', password='root')
        Installer.create_standard_heads()

    @staticmethod
    def create_standard_heads():
        db_session = Database.Session()
        order = 0
        headers = [{'title': 'Name', 'description': ''},
                   {'title': 'Spezies', 'description': ''},
                   {'title': 'Kultur', 'description': 'Regionale Kultur'},
                   {'title': 'Profession', 'description': ''},
                   {'title': 'Größe', 'description': 'Größe in cm (oder Halbfinger)'},
                   {'title': 'Gewicht', 'description': ''},
                   {'title': 'Geschlecht', 'description': ''},
                   {'title': 'Haarfarbe', 'description': ''},
                   {'title': 'Augenfarbe', 'description': ''},
                   {'title': 'Geburtsdatum', 'description': ''},
                   {'title': 'Alter', 'description': 'Alter in Jahren'},
                   {'title': 'Geburtsort', 'description': ''},
                   {'title': 'Familie', 'description': 'Wichtige Verwandte'},
                   {'title': 'Titel', 'description': ''},
                   {'title': 'Sozialstatus', 'description': ''},
                   {'title': 'Charakteristika', 'description': 'Was macht den Charakter aus?'},
                   {'title': 'Sonstiges', 'description': ''}]
        for h in headers:
            ManagementController.create_head(db_session, h['title'], h['description'], order, True)
            order = order + 1
