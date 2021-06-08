from builder import Builder
from ui_tests.ui.locators.pages_locators import RegistrationPageLocators
from ui_tests.ui.pages.base_page import BasePage


builder = Builder()


class RegistrationPage(BasePage):

    locators = RegistrationPageLocators()

    def open_login_page(self):
        self.click(self.locators.OPEN_LOGIN_PAGE_LOCATOR)

    def register_user(self, username=None, email=None, password=None, confirm_password=None):
        user = builder.create_user(username, email, password)
        self.write_text(self.locators.USERNAME_FIELD_LOCATOR, user.username)
        self.write_text(self.locators.EMAIL_FIELD_LOCATOR, user.email)
        self.write_text(self.locators.USER_PASSWORD_FIELD_LOCATOR, user.password)
        if confirm_password is None:
            confirm_password = user.password
        self.write_text(self.locators.CONFIRM_PASSWORD_FIELD_LOCATOR, confirm_password)
        self.click(self.locators.ACCEPTANCE_CHECKBOX_LOCATOR)
        self.click(self.locators.REGISTER_BUTTON_LOCATOR)
        return user

    def register_user_no_accept(self, username=None, email=None, password=None, confirm_password=None):
        user = builder.create_user(username, email, password)
        print(user.username, user.email, user.password)
        self.write_text(self.locators.USERNAME_FIELD_LOCATOR, user.username)
        self.write_text(self.locators.EMAIL_FIELD_LOCATOR, user.email)
        self.write_text(self.locators.USER_PASSWORD_FIELD_LOCATOR, user.password)
        if confirm_password is None:
            confirm_password = user.password
        self.write_text(self.locators.CONFIRM_PASSWORD_FIELD_LOCATOR, confirm_password)
        self.click(self.locators.REGISTER_BUTTON_LOCATOR)




