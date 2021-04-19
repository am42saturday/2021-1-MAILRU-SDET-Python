import allure

from hw2.ui.locators.pages_locators import LoginPageLocators
from hw2.ui.pages.base_page import BasePage
from hw2.data import BASE_TIMEOUT


class LoginPage(BasePage):

    locators = LoginPageLocators()

    @allure.step('Авторизация')
    def login(self, email, password):
        self.click(self.locators.LOGIN_BUTTON_LOCATOR, timeout=BASE_TIMEOUT)
        self.write_text(self.locators.LOGIN_FIELD_LOCATOR, email)
        self.write_text(self.locators.PASSWORD_FIELD_LOCATOR, password)
        self.click(self.locators.LOGIN_LOCATOR, timeout=BASE_TIMEOUT)

    @allure.step('Логаут')
    def logout(self):
        self.click(self.locators.USER_LOCATOR,
                   timeout=BASE_TIMEOUT)
        self.click(self.locators.LOGOFF_BUTTON_LOCATOR, timeout=BASE_TIMEOUT)
