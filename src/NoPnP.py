import configparser


class NoPnP:
    def __init__(self, arguments=None):
        configfile = 'nopnp.conf'
        if arguments is not None:
            status = 'n'
            for arg in arguments:
                if status == 'n':
                    if arg == '-c':
                        status = 'c'
                elif status == 'c':
                    configfile = arg

        self.config = self.load_config(configfile)

    @staticmethod
    def load_config(filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config
