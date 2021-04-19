import pytest

from hw3.utils.builder import Builder
from hw3.utils.data import user_login, user_password


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.builder = Builder()
        self.api_client = api_client

        if self.authorize:
            res, self.csrftoken = self.api_client.post_login(user_login, user_password)
