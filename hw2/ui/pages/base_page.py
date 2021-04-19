import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from hw2.ui.locators.pages_locators import BasePageLocators
from hw2.data import CLICK_RETRY, BASE_TIMEOUT, BASE_PERIOD


class BasePage(object):

    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=BASE_TIMEOUT):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_on_page(self, text, timeout=BASE_TIMEOUT, period=BASE_PERIOD):
        _time = 0
        while _time < timeout:
            if text in self.driver.page_source:
                return True
            time.sleep(period)
            _time += period
        return False

    def check_absense_on_page(self, text, timeout=BASE_TIMEOUT, period=BASE_PERIOD):
        _time = 0
        while _time < timeout:
            if text not in self.driver.page_source:
                return True
            time.sleep(period)
            _time += period
        return False

    def wait(self, timeout=BASE_TIMEOUT) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=BASE_TIMEOUT):
        for i in range(CLICK_RETRY):
            try:
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def write_text(self, locator, text):
        input_field = self.find(locator)
        input_field.clear()
        input_field.send_keys(text)

    def upload_file(self, locator, path):
        self.find(locator).send_keys(path)

    def refresh_page(self):
        self.driver.refresh()

