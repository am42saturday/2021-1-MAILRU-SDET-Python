import logging
from urllib.parse import urljoin

import allure
import requests

from builder import Builder

logger = logging.getLogger('test')
builder = Builder()

MAX_RESPONSE_LENGTH = 500


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    @staticmethod
    def log_pre(method, url, headers, data, params):
        logger.info(f'Performing {method} request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'PARAMS: {params}\n\n')

    @staticmethod
    def log_post(response):
        log_str = 'Got response:\n' \
                  f'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n')
            elif logger.level == logging.DEBUG:
                logger.debug(f'{log_str}\n'
                             f'RESPONSE CONTENT: {response.text}\n\n')
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n\n')

    def _request(self, method, url, headers=None, data=None, params=None):
        self.log_pre(method, url, headers, data, params)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            }
        response = self.session.request(method, url, headers=headers, data=data, params=params)
        self.log_post(response)
        return response

    @allure.step('Авторизация')
    def post_login(self, username, password):
        location = urljoin(self.base_url, '/login')

        headers = {
            'Referer': location,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        data = {'username': username,
                'password': password,
                'submit': 'Login'}

        result = self._request('POST', location, headers=headers, data=data)

        return result

    @allure.step('Регистрация')
    def post_register(self, username=None, email=None, password=None, confirm_password=None, term='y'):
        user = builder.create_user(username, email, password)

        location = urljoin(self.base_url, '/reg')

        headers = {
            'Referer': location,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        if confirm_password is None:
            confirm_password = user.password

        data = {
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'confirm': confirm_password,
            'term': term,
            'submit': 'Register'
        }

        result = self._request('POST', location, headers=headers, data=data)

        return user, result

    @allure.step('Выход из сессии пользователя')
    def get_logout(self):
        location = urljoin(self.base_url, '/logout')

        headers = {
            'Referer': self.base_url + '/welcome/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        result = self._request('GET', location, headers=headers)

        return result

    @allure.step('Получить статус приложения')
    def get_app_status(self):
        location = urljoin(self.base_url, '/status')

        headers = {
            'Content-Type': 'application/json',
        }

        result = self._request('GET', location, headers=headers)

        return result

    @allure.step('Создать пользователя')
    def post_add_user(self, username=None, email=None, password=None):
        user = builder.create_user(username, email, password)

        location = urljoin(self.base_url, '/api/add_user')

        headers = {
            'Content-Type': 'application/json',
            'Referer': location,
            'Accept-Encoding': 'gzip, deflate, br',
        }

        data = '{"username":"%s","password":"%s","email":"%s"}' % (user.username, user.password, user.email)

        result = self._request('POST', location, headers=headers, data=data)

        return user, result

    @allure.step('Удалить пользователя')
    def get_delete(self, username):
        location = urljoin(self.base_url, '/api/del_user/' + username)

        headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        result = self._request('GET', location, headers=headers)

        return result

    @allure.step('Заблокировать пользователя')
    def get_block_user(self, username):
        location = urljoin(self.base_url, '/api/block_user/' + username)

        headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        result = self._request('GET', location, headers=headers)

        return result

    @allure.step('Разблокировать пользователя')
    def get_unblock_user(self, username):
        location = urljoin(self.base_url, '/api/accept_user/' + username)

        headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        result = self._request('GET', location, headers=headers)

        return result



