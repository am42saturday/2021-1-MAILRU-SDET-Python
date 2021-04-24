import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import element_to_be_clickable

from hw2.data import BASE_TIMEOUT, link_for_campaign, campaign_image_path
from hw2.ui.locators.pages_locators import CampaignsPageLocators
from hw2.ui.pages.base_page import BasePage


class CampaignsPage(BasePage):

    locators = CampaignsPageLocators()

    @allure.step('Открыть страницу Campaigns')
    def open_campaigns_page(self):
        self.click(self.locators.CAMPAIGNS_LOCATOR, timeout=BASE_TIMEOUT)
        return self

    @allure.step('Создать новую кампанию')
    def open_create_new_campaign(self):
        try:
            self.click(self.locators.CREATE_ANOTHER_CAMPAIGN_LOCATOR, timeout=BASE_TIMEOUT)
        except TimeoutException:
            self.click(self.locators.CREATE_THE_CAMPAIGN_LOCATOR, timeout=BASE_TIMEOUT)

    @allure.step('Заполнить данные новой кампании')
    def fill_in_campaign_data(self, title):
        self.click(self.locators.CAMPAIGN_OBJECTIVE_REACH_LOCATOR, timeout=BASE_TIMEOUT)

        self.write_text(self.locators.LINK_FIELD_LOCATOR, link_for_campaign)
        self.wait(BASE_TIMEOUT).until(element_to_be_clickable(self.locators.CAMPAIGN_NAME_FIELD_LOCATOR))
        self.write_text(self.locators.CAMPAIGN_NAME_FIELD_LOCATOR, title)
        self.click(self.locators.CHOOSE_BANNER_AD_FORMAT, timeout=BASE_TIMEOUT)

        try:
            self.upload_file(self.locators.UPLOAD_IMAGE_LOCATOR, campaign_image_path)
        except:
            pass
        self.click(self.locators.SAVE_AD_LOCATOR, timeout=BASE_TIMEOUT)

    @allure.step('Создать кампанию')
    def create_campaign(self, title):
        self.fill_in_campaign_data(title)
        self.click(self.locators.CREATE_CAMPAIGN_LOCATOR)

    @allure.step('Удалить кампанию')
    def delete_campaign(self, title):
        self.click((self.locators.CHOOSE_CAMPAIGN_FROM_LIST_LOCATOR[0],
                    self.locators.CHOOSE_CAMPAIGN_FROM_LIST_LOCATOR[1].format(title)), timeout=BASE_TIMEOUT)
        self.click(self.locators.CAMPAIGN_LIST_ACTIONS_LOCATOR, timeout=BASE_TIMEOUT)
        self.click(self.locators.REMOVE_CHOSEN_CAMPAIGNS_LOCATOR, timeout=BASE_TIMEOUT)
        self.refresh_page()
