from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_BUTTON_LOCATOR = (By.XPATH, './/div[text()="Войти"]')
    USER_LOCATOR = (By.XPATH, './/div[text()="Balance: "]')
    LOGOFF_BUTTON_LOCATOR = (By.XPATH, './/a[@href="/logout"]')


class LoginPageLocators(BasePageLocators):
    LOGIN_FIELD_LOCATOR = (By.NAME, 'email')
    PASSWORD_FIELD_LOCATOR = (By.NAME, 'password')
    LOGIN_LOCATOR = (By.XPATH, './/div[contains(@class, "authForm-module-button")]')


class AudiencesPageLocators(BasePageLocators):
    AUDIENCES_LOCATOR = (By.XPATH, './/a[@href="/segments"]')
    CREATE_NEW_SEGMENT_LOCATOR = (By.XPATH, './/a[@href="/segments/segments_list/new/"]')
    CREATE_ANOTHER_SEGMENT = (By.XPATH, './/div[text()="Create segment"]')
    APPS_AND_GAMES_IN_SOCIAL_NETWORKS_LOCATOR = (By.XPATH, './/div[text()="Apps and games in social networks"]')
    PAID_AND_PLAYED_LOCATOR = (By.XPATH, './/div[@class="adding-segments-source"]/div/input')
    SEGMENT_NAME_LOCATOR = (By.XPATH, './/div[@class="input input_create-segment-form"]//input')
    ADD_SEGMENT_LOCATOR = (By.XPATH, './/div[text()="Add segment"]')
    CREATE_SEGMENT_LOCATOR = (By.XPATH, './/div[text()="Create segment"]')
    CHOOSE_SEGMENT_FROM_LIST_LOCATOR = (By.XPATH, './/a[@title="{}"]/../../..//input[@type="checkbox"]')
    SEGMENTS_LIST_ACTIONS_LOCATOR = (By.XPATH, './/span[text()="Actions"]')
    REMOVE_CHOSEN_SEGMENTS_LOCATOR = (By.XPATH, './/li[text()="Remove"]')


class CampaignsPageLocators(BasePageLocators):
    CAMPAIGNS_LOCATOR = (By.XPATH, './/a[@href="/dashboard"]')
    CREATE_THE_CAMPAIGN_LOCATOR = (By.XPATH, './/a[@href="/campaign/new"]')
    CREATE_ANOTHER_CAMPAIGN_LOCATOR = (By.XPATH, './/div[text()="Create campaign"]')
    CAMPAIGN_OBJECTIVE_REACH_LOCATOR = (By.XPATH, './/div[text()="Reach"]')
    LINK_FIELD_LOCATOR = (By.XPATH, './/input[@data-gtm-id="ad_url_text"]')
    CAMPAIGN_NAME_FIELD_LOCATOR = (By.XPATH, './/div[contains(@class,"input_campaign-name")]//input')
    CHOOSE_BANNER_AD_FORMAT = (By.XPATH, './/div[@id="patterns_4"]')
    UPLOAD_IMAGE_LOCATOR = (By.XPATH, './/input[@data-test="image_240x400"]')
    SAVE_AD_LOCATOR = (By.XPATH, './/div[text()="Save ad"]')
    CREATE_CAMPAIGN_LOCATOR = (By.XPATH, './/div[text()="Create a campaign"]')
    CHOOSE_CAMPAIGN_FROM_LIST_LOCATOR = (By.XPATH, './/a[@title="{}"]/../input')
    CAMPAIGN_LIST_ACTIONS_LOCATOR = (By.XPATH, './/span[text()="Actions"]')
    REMOVE_CHOSEN_CAMPAIGNS_LOCATOR = (By.XPATH, './/li[@title="Delete"]')



