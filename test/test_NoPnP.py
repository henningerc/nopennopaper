import pytest
import src.NoPnP


class TestApp:
    def test_config_loads(self):
        app = src.NoPnP.NoPnP()
        assert 'Database' in app.config

    def test_database_config(self):
        app = src.NoPnP.NoPnP()
        assert app.config['Database']['server'] == 'localhost'

    def test_command_line_option_config(self):
        clo = ['nopnp.py', '-c', 'newConfig.conf']
        app_config = src.NoPnP.NoPnP(clo)
        assert 'NotRight' in app_config.config
