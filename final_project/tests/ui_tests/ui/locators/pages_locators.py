from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_FIELD_LOCATOR = (By.ID, 'username')
    PASSWORD_FIELD_LOCATOR = (By.ID, 'password')
    LOGIN_BUTTON_LOCATOR = (By.ID, 'submit')
    CREATE_AN_ACCOUNT_BUTTON = (By.XPATH, './/a[text()="Create an account"]')


class RegistrationPageLocators:
    USERNAME_FIELD_LOCATOR = (By.ID, 'username')
    EMAIL_FIELD_LOCATOR = (By.ID, 'email')
    USER_PASSWORD_FIELD_LOCATOR = (By.ID, 'password')
    CONFIRM_PASSWORD_FIELD_LOCATOR = (By.ID, 'confirm')
    ACCEPTANCE_CHECKBOX_LOCATOR = (By.ID, 'term')
    REGISTER_BUTTON_LOCATOR = (By.ID, 'submit')
    OPEN_LOGIN_PAGE_LOCATOR = (By.XPATH, './/a[text()="Log in"]')


class MainPageLocators:
    VERSION_BUTTON_LOCATOR = (By.XPATH, './/a[text()=" TM version 0.1"]')
    HOME_BUTTON_LOCATOR = (By.XPATH, './/a[text()="HOME"]')

    PYTHON_DROPDOWN_LOCATOR = (By.XPATH, './/a[text()="Python"]')
    PYTHON_HISTORY_BUTTON_LOCATOR = (By.XPATH, './/a[text()="Python history"]')
    ABOUT_FLASK_BUTTON_LOCATOR = (By.XPATH, './/a[text()="About Flask"]')

    LINUX_DROPDOWN_LOCATOR = (By.XPATH, './/a[text()="Linux"]')
    DOWNLOAD_CENTOS_BUTTON_LOCATOR = (By.XPATH, './/a[text()="Download Centos7"]')

    NETWORK_DROPDOWN_LOCATOR = (By.XPATH, './/a[text()="Network"]')
    WIRESHARK_NEWS_BUTTON_LOCATOR = (By.XPATH, './/a[text()="News"]')
    DOWNLOAD_WIRESHARK_BUTTON_LOCATOR = (By.XPATH, './/a[text()="Download"]')
    TCPDUMP_EXAMPLES_BUTTON_LOCATOR = (By.XPATH, './/a[text()="Examples "]')

    LOGGED_AS_TEXT_LOCATOR = (By.XPATH, './/div[@id="login-name"]//li[1]')
    VK_ID_TEXT_LOCATOR = (By.XPATH, './/div[@id="login-name"]//li[2]')
    LOGOUT_BUTTON_LOCATOR = (By.ID, 'logout')

    API_BUTTON_LOCATOR = (By.XPATH, './/div[text()="What is an API?"]/..//a')
    FUTURE_OF_INTERNET_BUTTON_LOCATOR = (By.XPATH, './/div[text()="Future of internet"]/..//a')
    SMTP_BUTTON_LOCATOR = (By.XPATH, './/div[text()="Lets talk about SMTP?"]/..//a')

    PYTHON_ZEN_TEXT_LOCATOR = (By.XPATH, './/p[text()="powered by ТЕХНОАТОМ"]/../p[2]')

