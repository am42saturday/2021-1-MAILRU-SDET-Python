import allure

from ui_tests.ui.locators.pages_locators import LoginPageLocators
from ui_tests.ui.pages.base_page import BasePage
from ui_tests.data import BASE_TIMEOUT


class LoginPage(BasePage):

    locators = LoginPageLocators()

    @allure.step('Успешная авторизация')
    def successful_login(self, username, password):
        self.write_text(self.locators.LOGIN_FIELD_LOCATOR, username)
        self.write_text(self.locators.PASSWORD_FIELD_LOCATOR, password)
        self.click(self.locators.LOGIN_BUTTON_LOCATOR, timeout=BASE_TIMEOUT)
        assert 'Logged as' in self.driver.page_source

    @allure.step('Неуспешная авторизация')
    def unsuccessful_login(self, username=None, password=None, error=''):
        self.write_text(self.locators.LOGIN_FIELD_LOCATOR, username)
        self.write_text(self.locators.PASSWORD_FIELD_LOCATOR, password)
        self.click(self.locators.LOGIN_BUTTON_LOCATOR, timeout=BASE_TIMEOUT)
        assert error in self.driver.page_source

    @allure.step('Открыть страницу регистрации')
    def open_registration_page(self):
        self.click(self.locators.CREATE_AN_ACCOUNT_BUTTON, timeout=BASE_TIMEOUT)
