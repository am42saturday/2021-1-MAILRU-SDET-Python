import allure

from ui_tests.data import BASE_TIMEOUT
from ui_tests.ui.locators.pages_locators import MainPageLocators
from ui_tests.ui.pages.base_page import BasePage


class MainPage(BasePage):

    locators = MainPageLocators()

    @allure.step('Open redirect page')
    def open_redirect_page(self, locators, expectation):
        if len(locators) == 1:
            self.click(locators[0])
        else:
            self.move_and_click(locators)

        tabs = []
        for handle in self.driver.window_handles:
            tabs.append(handle)
        assert len(tabs) == 2
        self.driver.switch_to_window(tabs[1])
        assert expectation in self.driver.page_source
        self.driver.switch_to_window(tabs[0])
        assert self.driver.current_url == 'http://127.0.0.1:8095/welcome/'

    @allure.step('Логаут')
    def logout(self):
        self.click(self.locators.LOGOUT_BUTTON_LOCATOR, timeout=BASE_TIMEOUT)

    @allure.step('Проверить отображение Дзена Питона')
    def check_zen_of_python_text(self):
        if self.get_text(self.locators.PYTHON_ZEN_TEXT_LOCATOR) == '':
            return False
        else:
            return True

    @allure.step('Нажать на кнопку Home')
    def click_home(self):
        self.click(self.locators.HOME_BUTTON_LOCATOR)

    @allure.step('Открыть выпадающее меню')
    def open_dropdow_menu(self, locator):
        self.click(locator)
        assert self.driver.current_url == 'http://127.0.0.1:8095/welcome/'
