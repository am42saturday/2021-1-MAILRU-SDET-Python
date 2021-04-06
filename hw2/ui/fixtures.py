import os

import allure
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from hw2.ui.pages.base_page import BasePage
from hw2.ui.pages.campaigns_page import CampaignsPage
from hw2.ui.pages.login_page import LoginPage
from hw2.ui.pages.audiences_page import AudiencesPage


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def audiences_page(driver, campaigns_page):
    return AudiencesPage(driver=driver)


@pytest.fixture
def campaigns_page(driver):
    return CampaignsPage(driver=driver)


@pytest.fixture(scope='function')
def driver(config):
    url = config['url']
    options = webdriver.ChromeOptions()
    manager = ChromeDriverManager(version='latest')
    browser = webdriver.Chrome(executable_path=manager.install(), options=options)
    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        allure.attach(driver.get_screenshot_as_png(), "Screenshot", allure.attachment_type.PNG)
        browser_logfile = os.path.join('browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

