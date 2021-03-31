from ui.locators.pages_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from data import BASE_TIMEOUT

class LoginPage(BasePage):

    locators = LoginPageLocators()

    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        self.click(self.locators.LOGIN_BUTTON_LOCATOR, timeout=BASE_TIMEOUT)
        self.write_text(self.locators.LOGIN_FIELD_LOCATOR, email)
        self.write_text(self.locators.PASSWORD_FIELD_LOCATOR, password)
        self.click(self.locators.LOGIN_LOCATOR, timeout=BASE_TIMEOUT)

    def logout(self):
        self.click(self.locators.USER_LOCATOR,
                   timeout=BASE_TIMEOUT)
        self.click(self.locators.LOGOFF_BUTTON_LOCATOR, timeout=BASE_TIMEOUT)
