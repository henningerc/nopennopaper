from src.views.users import UserView


class TestUserView:
    def test_user_view(self):
        test = UserView()
        value = test.login()
        assert "No Pen, No Paper: Login" in value
