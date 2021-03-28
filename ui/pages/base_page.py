import random
import string

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators.pages_locators import BasePageLocators
from data import CLICK_RETRY, BASE_TIMEOUT


class BasePage(object):

    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_on_page(self, text):
        for i in range(BASE_TIMEOUT):
            try:
                text in self.driver.page_source
                return True
            except TimeoutException:
                if i == BASE_TIMEOUT:
                    return False

    def wait(self, timeout=None):
        if timeout is None:
            timeout = BASE_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=None):
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
        input_field.send_keys(text)

    def generate_random_name(self, length):
        result = ''.join(random.choice(string.ascii_letters) for _ in range(length))
        return result

    def clear_text_field(self, locator):
        element = self.find(locator)
        element.clear()
