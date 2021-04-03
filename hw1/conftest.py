from hw1.ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    return {'url': url}
