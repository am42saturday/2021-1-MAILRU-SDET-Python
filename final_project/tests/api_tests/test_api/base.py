import pytest

from builder import Builder


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, mysql_client):
        self.builder = Builder()
        self.mysql_client = mysql_client
        self.api_client = api_client
        self.base_user, res = self.api_client.post_register()

        if not self.authorize:
            self.api_client.get_logout()

