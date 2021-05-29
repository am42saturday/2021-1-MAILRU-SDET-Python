import logging
import os
import shutil
import signal
import subprocess
import time
from copy import copy

import pytest
import requests
from requests.exceptions import ConnectionError

from hw7 import settings

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


def waiter(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError('App did not started in 5s!')


def start_app(config):
    app_path = os.path.join(repo_root, 'app', 'app.py')

    app_out = open('app_stdout.log', 'w')
    app_err = open('app_stderr.log', 'w')

    env = copy(os.environ)
    env['APP_HOST'] = settings.APP_HOST
    env['APP_PORT'] = settings.APP_PORT

    env['STUB_HOST'] = settings.STUB_HOST
    env['STUB_PORT'] = settings.STUB_PORT

    env['MOCK_HOST'] = settings.MOCK_HOST
    env['MOCK_PORT'] = settings.MOCK_PORT

    proc = subprocess.Popen(['python3', app_path], stdout=app_out, stderr=app_err, env=env)

    config.app_proc = proc
    config.app_out = app_out
    config.app_err = app_err

    waiter(settings.APP_HOST, settings.APP_PORT)


def start_stub(config):
    stub_path = os.path.join(repo_root, 'stub', 'simple_http_server_stub.py')

    stub_out = open('stub_stdout.log', 'w')
    stub_err = open('stub_stderr.log', 'w')

    env = copy(os.environ)
    env['STUB_HOST'] = settings.STUB_HOST
    env['STUB_PORT'] = settings.STUB_PORT

    proc = subprocess.Popen(['python3', stub_path], stdout=stub_out, stderr=stub_err, env=env)

    config.stub_proc = proc
    config.stub_out = stub_out
    config.stub_err = stub_err

    waiter(settings.STUB_HOST, settings.STUB_PORT)


def start_mock():
    from hw7.mock import flask_mock
    flask_mock.run_mock()

    env = copy(os.environ)
    env['MOCK_HOST'] = settings.MOCK_HOST
    env['MOCK_PORT'] = settings.MOCK_PORT

    waiter(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        start_mock()
        start_stub(config)
        start_app(config)


def stop_app(config):
    config.app_proc.send_signal(signal.SIGINT)
    exit_code = config.app_proc.wait()

    config.app_out.close()
    config.app_err.close()

    assert exit_code == 0


def stop_stub(config):
    config.stub_proc.send_signal(signal.SIGINT)
    config.stub_proc.wait()

    config.stub_out.close()
    config.stub_err.close()


def stop_mock():
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_app(config)
        stop_stub(config)
        stop_mock()


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(os.path.abspath('tests_logs'), test_name)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG

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
