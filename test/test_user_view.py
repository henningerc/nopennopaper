from src.views.users import UserView


class TestUserView:
    def test_user_view(self):
        test = UserView()
        test.login()
