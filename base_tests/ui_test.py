import pytest

from base_tests.base import BaseCase
from data import email, password, user_name, user_email
from ui.locators.pages_locators import MainPageLocators
from data import BASE_TIMEOUT, BASE_PERIOD
from ui.utils import generate_random_name


class TestOne(BaseCase):

    # Тест на логин
    @pytest.mark.UI
    def test_login(self):
        self.login_page.login(email, password)
        assert self.base_page.find_on_page('How to get started?', BASE_TIMEOUT, BASE_PERIOD)

    # Тест на логаут
    @pytest.mark.UI
    def test_logout(self):
        self.login_page.login(email, password)
        self.main_page.click(self.main_page.locators.PROFILE_LOCATOR)
        self.login_page.logout()
        assert self.base_page.find_on_page('Рекламируйте товары и услуги в соцсетях', BASE_TIMEOUT, BASE_PERIOD)

    # Тест на редактирование контактной информации в профиле
    @pytest.mark.UI
    def test_change_contact_info(self):
        self.login_page.login(email, password)
        self.main_page.click(self.main_page.locators.PROFILE_LOCATOR)
        new_user_name = user_name + generate_random_name(5)
        new_user_email = generate_random_name(5) + user_email
        self.main_page.change_user_info(new_user_name, new_user_email)
        assert new_user_name == self.main_page.get_element_text(self.main_page.locators.USER_NAME_LOCATOR)
        assert new_user_email == self.main_page.get_element_text(self.main_page.locators.USER_EMAIL_LOCATOR)

    # Тест на переход на страницы портала
    @pytest.mark.parametrize(
        'menu_item, opened_page_text',
        [
            (MainPageLocators.PROFILE_LOCATOR, 'Contact information'),
            (MainPageLocators.STATISTICS_LOCATOR, 'You do not have any ad campaigns yet.')
        ]
    )
    @pytest.mark.UI
    def test_menu_items(self, menu_item, opened_page_text):
        self.login_page.login(email, password)
        self.main_page.click(menu_item)
        assert self.base_page.find_on_page(opened_page_text, BASE_TIMEOUT, BASE_PERIOD)
