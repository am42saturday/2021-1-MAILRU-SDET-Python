from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_BUTTON_LOCATOR = (By.XPATH, './/div[text()="Войти"]')
    USER_LOCATOR = (By.XPATH, './/div[text()="Balance: "]')
    LOGOFF_BUTTON_LOCATOR = (By.XPATH, './/a[@href="/logout"]')


class LoginPageLocators(BasePageLocators):
    LOGIN_FIELD_LOCATOR = (By.NAME, 'email')
    PASSWORD_FIELD_LOCATOR = (By.NAME, 'password')
    LOGIN_LOCATOR = (By.XPATH, './/div[contains(@class, "authForm-module-button")]')


class MainPageLocators(BasePageLocators):
    PROFILE_LOCATOR = (By.XPATH, './/a[@href="/profile"]')
    STATISTICS_LOCATOR = (By.XPATH, './/a[@href="/statistics"]')
    USER_NAME_LOCATOR = (By.XPATH, './/div[@data-name="fio"]//input[@class="input__inp js-form-element"]')
    USER_EMAIL_LOCATOR = (By.XPATH, './/div[@data-class-name="AdditionalEmailRow"]//'
                                    'input[@class="input__inp js-form-element"]')
    SAVE_BUTTON_LOCATOR = (By.XPATH, './/button[@class="button button_submit"]')
