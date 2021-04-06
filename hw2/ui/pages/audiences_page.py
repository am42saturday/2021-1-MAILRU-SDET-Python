import allure
from selenium.common.exceptions import TimeoutException

from hw2.ui.pages.base_page import BasePage
from hw2.ui.locators.pages_locators import AudiencesPageLocators
from hw2.data import BASE_TIMEOUT


class AudiencesPage(BasePage):

    locators = AudiencesPageLocators()

    @allure.step('Открыть страницу Audiences')
    def open_audiences_page(self):
        self.click(self.locators.AUDIENCES_LOCATOR, timeout=BASE_TIMEOUT)

    @allure.step('Открыть создание сегмента в аудиториях')
    def create_audience_segment(self):
        try:
            self.click(self.locators.CREATE_NEW_SEGMENT_LOCATOR, timeout=BASE_TIMEOUT)
        except TimeoutException:
            self.click(self.locators.CREATE_ANOTHER_SEGMENT, timeout=BASE_TIMEOUT)

    @allure.step('Заполнить данные сегмента')
    def fill_in_segment_data(self, choose_segment_locator, title):
        self.click(choose_segment_locator, timeout=BASE_TIMEOUT)
        self.click(self.locators.PAID_AND_PLAYED_LOCATOR, timeout=BASE_TIMEOUT)
        self.click(self.locators.ADD_SEGMENT_LOCATOR, timeout=BASE_TIMEOUT)
        self.write_text(self.locators.SEGMENT_NAME_LOCATOR, title)
        self.click(self.locators.CREATE_SEGMENT_LOCATOR, timeout=BASE_TIMEOUT)

    @allure.step('Удалить сегмент')
    def delete_segment(self, title):
        self.click((self.locators.CHOOSE_SEGMENT_FROM_LIST_LOCATOR[0],
                    self.locators.CHOOSE_SEGMENT_FROM_LIST_LOCATOR[1].format(title)), timeout=BASE_TIMEOUT)
        self.click(self.locators.SEGMENTS_LIST_ACTIONS_LOCATOR, timeout=BASE_TIMEOUT)
        self.click(self.locators.REMOVE_CHOSEN_SEGMENTS_LOCATOR, timeout=BASE_TIMEOUT)


