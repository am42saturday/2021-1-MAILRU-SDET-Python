import pytest

from hw6.mysql.client import MysqlClient


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
        mysql_client.recreate_db()

        mysql_client.connect()
        mysql_client.create_all_requests()
        mysql_client.create_requests_by_method()
        mysql_client.create_top_10_frequent_requests()
        mysql_client.create_top_5_largest_4xx_requests()
        mysql_client.create_top_5_users_5xx_request()

        mysql_client.connection.close()
