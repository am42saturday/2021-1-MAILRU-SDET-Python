import json

import allure
import pytest

from hw3.test_api.base import ApiBase
from hw3.utils.data import user_login, user_password
from hw3.utils.builder import Builder


class TestAuth(ApiBase):
    authorize = False

    @pytest.mark.API('API')
    @allure.title('Успешная авторизация')
    def test_valid_login(self):
        self.api_client.post_login(user_login, user_password)


class TestSegment(ApiBase):

    @pytest.mark.API('API')
    @allure.title('Тест на создание сегмента')
    def test_create_segment(self):
        segment_name = Builder.create_title()
        response, segment_id = self.api_client.create_segment(segment_name)

        # Check created segment exists
        response = self.api_client.open_segment(segment_id)
        assert response['items'][0]['status'] != 'not found'

        # Delete test segment
        self.api_client.delete_segment(segment_id)

    @pytest.mark.API('API')
    @allure.title('Тест на удаление сегмента')
    def test_delete_segment(self):
        segment_name = Builder.create_title()
        res, segment_id = self.api_client.create_segment(segment_name)

        response = self.api_client.delete_segment(segment_id)
        assert not response['errors']

        # Check deleted segment not found
        response = self.api_client.open_segment(segment_id)
        assert response['items'][0]['status'] == 'not found'



