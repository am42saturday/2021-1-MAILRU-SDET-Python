import pytest
from selenium import webdriver
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage


@pytest.fixture
def base_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture(scope='function')
def driver(config):
    url = config['url']
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options, executable_path='/home/mary/Downloads/chromedriver')
    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()
