import logging
import os
import shutil
import allure
import pytest

from api_tests.api.client import ApiClient
from api_tests.api.mysql_client import MysqlClient
from api_tests.utils.data import dir_for_test_logs
from ui_tests.ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--url', default='http://127.0.0.1:8095')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--browser', default='chrome')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    if request.config.getoption('--selenoid'):
        selenoid = 'http://127.0.0.1:4444'
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
    else:
        selenoid = None
        vnc = False

    browser = request.config.getoption('--browser')
    debug_log = request.config.getoption('--debug_log')
    return {'url': url, 'browser': browser, 'debug_log': debug_log, 'selenoid': selenoid, 'vnc': vnc}


@pytest.fixture(scope='function')
def api_client(config):
    return ApiClient(config['url'])


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient()
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(dir_for_test_logs, (test_name if len(test_name) < 100 else test_name[:100]))
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)

