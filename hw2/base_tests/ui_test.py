import allure
import pytest

from hw2.base_tests.base import BaseCase
from hw2.data import email, wrong_password, invalid_login, wrong_email
from hw2.ui.utils import generate_random_name


class TestInvalidLogin(BaseCase):
    authorize = False

    @pytest.mark.parametrize(
        'login, passwd, expected_result',
        [
            (email, wrong_password, 'Invalid login or password'),
            (wrong_email, wrong_password, 'Invalid login or password'),
            (invalid_login, wrong_password, 'Введите email или телефон'),
        ]
    )
    @pytest.mark.UI
    @allure.title('Негативный тест на авторизацию')
    @allure.description('Негативный тест на авторизацию')
    def test_unsuccessful_login(self, login, passwd, expected_result):
        self.login_page.login(login, passwd)
        assert self.login_page.find_on_page(expected_result)


class TestCampaigns(BaseCase):
    @pytest.mark.UI
    @allure.title('Создание рекламной кампании')
    def test_create_campaign(self):
        self.campaigns_page.open_create_new_campaign()
        campaign_title = 'Campaign ' + generate_random_name(5)
        self.campaigns_page.fill_in_campaign_data(campaign_title)
        self.campaigns_page.create_campaign()
        assert self.audiences_page.find_on_page('Active campaigns')
        assert self.audiences_page.find_on_page(campaign_title)
        self.campaigns_page.delete_campaign(campaign_title)
        assert self.audiences_page.check_absense_on_page(campaign_title)


class TestAudiences(BaseCase):
    @pytest.mark.UI
    @allure.title('Создание сегмента в аудиториях')
    @allure.description('Тест на создание сегмента в аудиториях и проверка, что сегмент создан')
    def test_create_audience_segment(self):
        self.audiences_page.open_audiences_page()
        self.audiences_page.create_audience_segment()
        segment_title = 'Segment ' + generate_random_name(5)
        self.audiences_page.fill_in_segment_data(self.audiences_page.locators.APPS_AND_GAMES_IN_SOCIAL_NETWORKS_LOCATOR,
                                                 segment_title)
        assert self.audiences_page.find_on_page('Segments list')
        assert self.audiences_page.find_on_page(segment_title)
        self.audiences_page.delete_segment(segment_title)

    @pytest.mark.UI
    @allure.title('Удаление сегмента в аудиториях')
    @allure.description('Тест на удаление сегмента в аудиториях и проверка, что сегмент удален')
    def test_delete_audience_segment(self):
        self.audiences_page.open_audiences_page()
        self.audiences_page.create_audience_segment()
        segment_title = 'Segment ' + generate_random_name(5)
        self.audiences_page.fill_in_segment_data(self.audiences_page.locators.APPS_AND_GAMES_IN_SOCIAL_NETWORKS_LOCATOR,
                                                 segment_title)
        assert self.audiences_page.find_on_page('Segments list')
        self.audiences_page.delete_segment(segment_title)
        assert self.audiences_page.check_absense_on_page(segment_title)

