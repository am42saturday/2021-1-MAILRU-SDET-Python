import pytest
from _pytest.fixtures import FixtureRequest

from hw2.data import password, email
from hw2.ui.pages.base_page import BasePage
from hw2.ui.pages.login_page import LoginPage
from hw2.ui.pages.audiences_page import AudiencesPage
from hw2.ui.pages.campaigns_page import CampaignsPage


class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        if self.authorize:
            self.login_page.login(email, password)
            self.audiences_page: AudiencesPage = request.getfixturevalue('audiences_page')
            self.campaigns_page: CampaignsPage = request.getfixturevalue('campaigns_page')
