import configparser


class NoPnP:
    def __init__(self):
        self.config = self.load_config()

    @staticmethod
    def load_config():
        config = configparser.ConfigParser()
        config.read('nopnp.conf')
        return config
