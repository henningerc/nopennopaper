import src.NoPnP


class TestApp:
    def test_no_pnp(self):
        app = src.NoPnP.NoPnP()
        assert 'Database' in app.config
        assert app.config['Database']['server'] == 'localhost'
