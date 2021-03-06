from selenium.webdriver.remote.webelement import WebElement

from hw1.ui.pages.base_page import BasePage
from hw1.ui.locators.pages_locators import MainPageLocators
from hw1.data import BASE_TIMEOUT


class MainPage(BasePage):

    locators = MainPageLocators()

    def change_user_info(self, user_name, user_email) -> None:
        self.write_text(self.locators.USER_NAME_LOCATOR, user_name)
        self.write_text(self.locators.USER_EMAIL_LOCATOR, user_email)
        self.click(self.locators.SAVE_BUTTON_LOCATOR)

    def get_element_text(self, locator) -> str:
        element: WebElement = self.find(locator, timeout=BASE_TIMEOUT)
        return element.get_attribute("value")
