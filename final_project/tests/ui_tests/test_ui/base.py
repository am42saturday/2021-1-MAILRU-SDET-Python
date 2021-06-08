import pytest
from _pytest.fixtures import FixtureRequest

from ui_tests.ui.pages.base_page import BasePage
from ui_tests.ui.pages.login_page import LoginPage
from ui_tests.ui.pages.registration_page import RegistrationPage
from ui_tests.ui.pages.main_page import MainPage


class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')

        self.login_page.open_registration_page()
        self.base_user = self.registration_page.register_user()

        if not self.authorize:
            self.main_page.logout()
