from src.controllers.user_management import UserManager
from src.controllers.management_controller import ManagementController
from src.controllers.database_management import Database
from src.models.models import LAttribute, LSkill


class InstallController:
    @staticmethod
    def install():
        if not UserManager.exists('root'):
            UserManager.create(login='root', username='root', email='root@root.lan', password='root', role=10)
        InstallController.create_standard_heads()
        InstallController.create_standard_attributes()
        InstallController.create_standard_skills()

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

    @staticmethod
    def create_standard_attributes():
        order = 0
        db_session = Database.Session()
        attributes = [
            {'t': 'Mut', 's': 'MU', 'd': ''},
            {'t': 'Klugheit', 's': 'KL', 'd': ''},
            {'t': 'Intuition', 's': 'IN', 'd': ''},
            {'t': 'Charisma', 's': 'CH', 'd': ''},
            {'t': 'Fingerfertigkeit', 's': 'FF', 'd': ''},
            {'t': 'Gewandtheit', 's': 'GE', 'd': ''},
            {'t': 'Konstitution', 's': 'KO', 'd': ''},
            {'t': 'Körperkraft', 's': 'KK', 'd': ''},
        ]
        for a in attributes:
            attribute = LAttribute(title=a['t'], description=a['d'], short=a['s'], order=order, standard=True)
            db_session.add(attribute)
            order += 1
        db_session.commit()

    @staticmethod
    def create_standard_skills():
        order = 0
        attributes = {}
        db_session = Database.Session()
        q_attributes = db_session.query(LAttribute).all()
        for qa in q_attributes:
            attributes[qa.short] = qa
        skills = [
            {'t': 'Fliegen', 'd': '', 'a1': 'MU', 'a2': 'IN', 'a3': 'GE'},
        ]
        for s in skills:
            skill = LSkill(title=s['t'], description=s['d'], attribute_1=attributes[s['a1']],
                           attribute_2=attributes[s['a2']], attribute_3=attributes[s['a3']], order=order, standard=True)
            db_session.add(skill)
            order += 1
        db_session.commit()
