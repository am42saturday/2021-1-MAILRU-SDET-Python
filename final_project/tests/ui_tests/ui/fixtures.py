import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from ui_tests.ui.pages.base_page import BasePage
from ui_tests.ui.pages.main_page import MainPage
from ui_tests.ui.pages.login_page import LoginPage
from ui_tests.ui.pages.registration_page import RegistrationPage
from ui_tests.data import tests_logs_dir


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def registration_page(driver):
    return RegistrationPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


def get_driver(config, download_dir):
    browser_name = config['browser']
    selenoid = config['selenoid']
    vnc = config['vnc']

    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')

        if selenoid is not None:
            options.add_experimental_option("prefs", {"download.default_directory": '/home/selenoid/Downloads'})
            options.add_experimental_option("prefs", {"profile.default_content_settings.popups": 0})
            options.add_experimental_option("prefs", {"download.prompt_for_download": False})
            caps = {'browserName': browser_name,
                    'version': '89.0',
                    'sessionTimeout': '2m'}

            if vnc:
                caps['version'] += '_vnc'
                caps['enableVNC'] = True

            browser = webdriver.Remote(selenoid + '/wd/hub', options=options, desired_capabilities=caps)

        else:
            options.add_experimental_option("prefs", {"download.default_directory": download_dir})
            manager = ChromeDriverManager(version='latest')
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)

    else:
        raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')

    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir, request: FixtureRequest):
    marker = request.node.get_closest_marker('UI')

    if marker is not None:
        url = config['url']
        browser = get_driver(config, download_dir=test_dir)

        browser.get(url)
        browser.maximize_window()
        yield browser
        browser.quit()
    else:
        yield 0


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request):
    if driver:
        test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
        if not os.path.isdir(tests_logs_dir):
            os.mkdir(tests_logs_dir)
        browser_logfile = os.path.join(tests_logs_dir, (test_name if len(test_name) < 100 else test_name[:100]))
        with open(browser_logfile + '/test.log', 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile + '/test.log', 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

        failed_tests_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_tests_count:
            allure.attach(driver.get_screenshot_as_png(), "Screenshot", allure.attachment_type.PNG)
    else:
        yield 0
