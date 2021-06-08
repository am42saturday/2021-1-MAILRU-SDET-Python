import json
import random
import string

import allure
import pytest

from api_tests.test_api.base import ApiBase
from api_tests.utils.models import TestUsersDB

EXISTING_USERNAME = object()
EXISTING_PASSWORD = object()
EXISTING_EMAIL = object()
CURRENT_USER = object()


class TestAPIUsers(ApiBase):
    """
    Тесты API

    Тест на проверку статуса приложения
    Тесты на успешное/неуспешное добавление пользователя
    Тесты на успешное/неуспешное удаление пользователя
    Тесты на успешное/неуспешное блокировку пользователя
    Тесты на успешное/неуспешное разблокировку пользователя
    """
    authorize = True

    @pytest.mark.API
    def test_api_check_app_status(self):
        """
        Тест на проверку статуса приложения
        Ожидается статус код 200
        """
        res = self.api_client.get_app_status()
        assert res.status_code == 200, f"Got status code {res.status_code}, expected 200"
        parsed_res = json.loads(res.content.decode())
        assert parsed_res['status'] == 'ok'

    @pytest.mark.API
    def test_api_requests_unauthorized(self):
        """
        Тест на попытку выполнить API запросы неавторизованным пользователем
        Ожидается статус код 401
        """
        self.api_client.get_logout()
        user, res = self.api_client.post_add_user()
        assert res.status_code == 401, f"Got status code {res.status_code}, expected 401"
        res_del = self.api_client.get_delete(self.base_user.username)
        assert res_del.status_code == 401, f"Got status code {res.status_code}, expected 401"
        res_block = self.api_client.get_block_user(self.base_user.username)
        assert res_block.status_code == 401, f"Got status code {res.status_code}, expected 401"
        res_unblock = self.api_client.get_block_user(self.base_user.username)
        assert res_unblock.status_code == 401, f"Got status code {res.status_code}, expected 401"

    @pytest.mark.API
    def test_api_add_user(self):
        """
        Тест на добавление пользователя

        Ожидается статус код 201
        Пользователь добавлен в бд
        """
        user, res = self.api_client.post_add_user()
        assert res.status_code == 201, f"Got status code {res.status_code}, expected 201"

        db_data = self.mysql_client.session.query(TestUsersDB).filter_by(username=user.username).all()
        assert len(db_data) == 1

    @pytest.mark.parametrize(
        'login, email, password',
        [
            (''.join(random.choice(string.ascii_letters) for i in range(3)), None, 'qazswxde'),
            ('TooLooongUsername', None, 'qazswxde'),
            (None, '', None),
            ('', '', ''),
            (None, 'tqwertyuiopqwertyuiopqwertyuiopqweetftuuhojikrxycfugyhtyuiopqwertyuiopest@emafhil.com', None),
            (None, ''.join(random.choice(string.ascii_letters) for i in range(3)), None),
            (None, ''.join(random.choice(string.ascii_letters) for i in range(10)), None),
            (None, None, ''),
            ('', None, None),
            (None, None, 'qwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwe'
                         'rtyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqw'
                         'ertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwerty'),
        ],
        ids=['short_username', 'long_username', 'empty_email', 'all_params_empty', 'long_email', 'short_email',
             'invalid_email', 'empty_pass', 'empty_username', 'long_pass']
    )
    @pytest.mark.API
    def test_api_negative_add_user(self, login, email, password):
        """
        Негативный тест на добавление пользователя

        :param login
        :param email
        :param password
        Ожидаемый статус код 400
        Пользователь не добавлен в бд
        """
        user, res = self.api_client.post_add_user(login, email, password)
        assert res.status_code == 400, f"Got status code {res.status_code}, expected 400"

        db_data = self.mysql_client.session.query(TestUsersDB).filter_by(username=login).all()
        assert len(db_data) == 0

    @pytest.mark.API
    @pytest.mark.parametrize(
        'login, email, password, expected_result',
        [
            (None, EXISTING_EMAIL, None, (304, 0)),
            (EXISTING_USERNAME, None, None, (304, 1)),
            (None, None, EXISTING_PASSWORD, (201, 1)),
        ],
        ids=['existing_email', 'existing_username', 'existing_pass']
    )
    def test_api_add_existing_user(self, login, email, password, expected_result):
        """
        Тест на повторное добавление существующего пользователя

        :param login
        :param email
        :param password
        :param expected_result
        Ожидаемый статус код содержится в expected_result
        Пользователь не добавлен в бд
        """
        if login == EXISTING_USERNAME:
            login = self.base_user.username
        if password == EXISTING_PASSWORD:
            password = self.base_user.password
        if email == EXISTING_EMAIL:
            email = self.base_user.email
        user, res = self.api_client.post_add_user(login, email, password)
        assert res.status_code == expected_result[0], \
            f"Got status code {res.status_code}, expected {expected_result[0]}"

        db_data = self.mysql_client.session.query(TestUsersDB).filter_by(username=login).all()
        assert len(db_data) == expected_result[1]

    @pytest.mark.parametrize(
        'login, expected_result',
        [
            (EXISTING_USERNAME, (204, '')),
            ('Not_existing', (404, 'User does not exist!')),
            ('', (404, '404')),
            (CURRENT_USER, (204, ''))
        ],
        ids=['existing_user', 'not_existing_user', 'empty_username_param', 'current_user']
    )
    @pytest.mark.API
    def test_api_delete_user(self, login, expected_result):
        """
        Тест на удаление пользователя

        :param login
        :param expected_result
        Ожидаемый статус код содержится в expected_result
        Пользователь не найден в бд
        """
        user, res = self.api_client.post_add_user()
        if login == EXISTING_USERNAME:
            login = user.username
        if login == CURRENT_USER:
            login = self.base_user.username
        res_del = self.api_client.get_delete(login)
        assert res_del.status_code == expected_result[0], \
            f"Got status code {res.status_code}, expected {expected_result[0]}"
        assert expected_result[1] in res_del.text

        db_data = self.mysql_client.session.query(TestUsersDB).filter_by(username=login).all()
        assert len(db_data) == 0

    @pytest.mark.parametrize(
        'login, expected_result',
        [
            (EXISTING_USERNAME, (200, 'User was blocked!')),
            ('Not_existing', (404, 'User does not exist!')),
            ('', (404, '404')),
            (CURRENT_USER, (200, 'User was blocked!'))
        ],
        ids=['existing_user', 'not_existing_user', 'empty_username_param', 'current_user']
    )
    @pytest.mark.API
    def test_api_block_user(self, login, expected_result):
        """
        Тест блокировки пользователя

        :param login
        :param expected_result
        Ожидаемый статус код содержится в expected_result
        Параметр access пользователя при успешной блокировке = 0
        """
        user, res = self.api_client.post_add_user()
        if login == EXISTING_USERNAME:
            login = user.username
        if login == CURRENT_USER:
            login = self.base_user.username
        res = self.api_client.get_block_user(login)
        assert res.status_code == expected_result[0], \
            f"Got status code {res.status_code}, expected {expected_result[0]}"
        assert expected_result[1] in expected_result[1]

        db_data = self.mysql_client.session.query(TestUsersDB).filter_by(username=login).all()
        if len(db_data):
            assert db_data[0].access == 0

    @pytest.mark.API
    def test_api_block_blocked_user(self):
        """
        Тест блокировки уже заблокированного пользователя

        Ожидаемый статус код 304
        Параметр access пользователя = 0
        """
        user, res = self.api_client.post_add_user()
        self.api_client.get_block_user(user.username)
        res = self.api_client.get_block_user(user.username)
        assert res.status_code == 304, f"Got status code {res.status_code}, expected 304"

        db_data = self.mysql_client.session.query(TestUsersDB).filter_by(username=user.username).all()
        if len(db_data):
            assert db_data[0].access == 0

    @pytest.mark.parametrize(
        'login, expected_result',
        [
            (EXISTING_USERNAME, (200, 'User access granted!')),
            ('Not_existing', (404, 'User does not exist!')),
            ('', (404, '404')),
            (CURRENT_USER, (304, ''))
        ],
        ids=['existing_user', 'not_existing_user', 'empty_username_param', 'current_user']
    )
    @pytest.mark.API
    def test_api_unblock_user(self, login, expected_result):
        """
        Тест на разблокировку пользователя

        :param login
        :param expected_result
        Ожидаемый статус код содержится в expected_result
        Параметр access пользователя при успешной разблокировке = 1
        """
        user, res = self.api_client.post_add_user()
        if login == EXISTING_USERNAME:
            login = user.username
            self.api_client.get_block_user(login)
        if login == CURRENT_USER:
            login = self.base_user.username
        res = self.api_client.get_unblock_user(login)
        assert res.status_code == expected_result[0], \
            f"Got status code {res.status_code}, expected {expected_result[0]}"
        assert expected_result[1] in res.text

        db_data = self.mysql_client.session.query(TestUsersDB).filter_by(username=login).all()
        if len(db_data):
            assert db_data[0].access == 1

    @pytest.mark.API
    def test_api_unblock_not_blocked_user(self):
        """
        Тест на разблокировку пользователя, который не заблокирован

        Ожидаемый статус код 304
        Параметр access пользователя = 1
        """
        user, res = self.api_client.post_add_user()
        res = self.api_client.get_unblock_user(user.username)
        assert res.status_code == 304, f"Got status code {res.status_code}, expected 304"

        db_data = self.mysql_client.session.query(TestUsersDB).filter_by(username=user.username).all()
        if len(db_data):
            assert db_data[0].access == 1


class TestAuth(ApiBase):
    """
    Тесты API на авторизацию

    Тест на успешную авторизацию
    Негативные тесты на авторизацию

    """
    authorize = False

    @pytest.mark.API('API')
    def test_api_successful_login(self):
        """
        Успешная авторизация

        Ожидаемый статус код 200
        """
        res = self.api_client.post_login(self.base_user.username, self.base_user.password)
        assert res.request.url == 'http://127.0.0.1:8095/welcome/'
        assert res.status_code == 200, f"Got status code {res.status_code}, expected 200"
        assert 'Logged as' in res.text

    @pytest.mark.parametrize(
        'login, password, expected_result',
        [
            ('', '', (200, 'Welcome to the TEST SERVER')),
            (EXISTING_USERNAME, '', (200, 'Welcome to the TEST SERVER')),
            ('', EXISTING_PASSWORD, (200, 'Welcome to the TEST SERVER')),
            ('wrong_login', 'wrong_password', (401, 'Invalid username or password')),
            (''.join(random.choice(string.ascii_letters) for i in range(2)), 'qazswxde', (401, 'Incorrect username length')),
            (''.join(random.choice(string.ascii_letters) for i in range(17)), 'qazswxde', (401, 'Incorrect username length')),
            (EXISTING_USERNAME, 'incorrect_pass', (401, 'Invalid username or password')),
            ('incorrect_name', EXISTING_PASSWORD, (401, 'Invalid username or password')),
        ],
        ids=['empty_login_and_pass', 'empty_pass', 'empty_login', 'wrong_login_and_pass', 'short_login', 'long_login',
             'wrong_pass', 'wrong_login']
    )
    @pytest.mark.API('API')
    def test_api_unsuccessful_login(self, login, password, expected_result):
        """
        Негативный тест на авторизацию

        :param login
        :param password
        :param expected_result
        Ожидаемый статус код содержится в expected_result
        """
        if login == EXISTING_USERNAME:
            login = self.base_user.username
        if password == EXISTING_PASSWORD:
            password = self.base_user.password
        res = self.api_client.post_login(login, password)
        assert res.status_code == expected_result[0], \
            f"Got status code {res.status_code}, expected {expected_result[0]}"
        assert expected_result[1] in res.text
        assert 'Test Server | Welcome!' not in res.text

    @pytest.mark.API
    @allure.description('')
    def test_api_logout(self):
        """
        Тест на выход из сессии пользователя

        Ожидаемый статус код 200
        """
        self.api_client.post_login(self.base_user.username, self.base_user.password)
        res = self.api_client.get_logout()
        assert res.status_code == 200, f"Got status code {res.status_code}, expected 200"
        assert 'Welcome to the TEST SERVER' in res.text


class TestRegistration(ApiBase):
    """
    Тесты API на регистрацию пользователя

    Тест на успешную регистрацию
    Тесты на регистрацию с невалидными данными
    Тесты на регистрацию уже существующего пользователя
    """
    authorize = False

    @pytest.mark.API
    def test_api_successful_registration(self):
        """
        Тест успешной регистрации пользователя

        Ожидаемый статус код 200
        """
        user, res = self.api_client.post_register()
        assert res.request.url == 'http://127.0.0.1:8095/welcome/'
        assert res.status_code == 200, f"Got status code {res.status_code}, expected 200"
        assert 'Logged as' in res.text

    @pytest.mark.parametrize(
        'login, email, password, confirm_pass, expected_result',
        [
            ('TooLooongUsername', None, 'qwerty', 'qwerty', 'Incorrect username length'),
            ('S', None, 'qazswxde', 'qazswxde', 'Incorrect username length'),
            (None, '', 'qazswxde', 'qazswxde', 'Incorrect email length'),
            (None, 'tqwertyuiopqwertyuiopqfgfwertyuiopqwertyuiopqwertyuiopest@email.com', 'qazswxde', 'qazswxde',
             'Incorrect email length'),
            (None, 'a@b.c', 'qazswxde', 'qazswxde', 'Incorrect email length'),
            (None, 'test.ru', 'qazswxde', 'qazswxde', 'Invalid email address'),
            (None, 'test@ru', 'qazswxde', 'qazswxde', 'Invalid email address'),
            (None, 'testwertyuiru', 'qazswxde', 'qazswxde', 'Invalid email address'),
            (None, None, 'qazswxde', '', 'Passwords must match'),
            (None, None, 'qazswxde', 'qazswxd', 'Passwords must match'),
            (None, None, 'qwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwe'
                         'rtyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqw'
                         'ertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwerty',
             None, 'Incorrect password length'),
            (None, None, '', 'qazswxde', 'Registration'),
            ('', None, 'qazswxde', 'qazswxde', 'Registration')
        ],
        ids=['long_name', 'short_name', 'empty_email', 'long_email', 'short_email', 'invalid_email_at',
             'invalid_email_point', 'invalid_email', 'empty_confirm_pass', 'not_matching_passwords', 'long_pass',
             'empty_pass', 'empty_username']
    )
    @pytest.mark.API
    def test_api_registration_invalid_data(self, login, email, password, confirm_pass, expected_result):
        """
        Тест регистрации пользователя с невалидными данными

        :param login
        :param email
        :param password
        :param confirm_pass
        :param expected_result
        Ожидаемый статус код содержится в expected_result
        """
        self.user, res = self.api_client.post_register(login, email, password, confirm_pass)
        assert res.status_code == 400, f"Got status code {res.status_code}, expected 400"
        assert expected_result in res.text
        assert 'Test Server | Welcome!' not in res.text

    @pytest.mark.parametrize(
        'term',
        ['', 'n', 123],
        ids=['empty_term', 'term_n', 'term_123']
    )
    @pytest.mark.API
    def test_api_registration_without_acceptance(self, term):
        """
        Тест регистрации пользователя невалидное значение принятия согласия

        :param term
        Ожидаемый статус код 400
        """
        self.user, res = self.api_client.post_register(term=term)
        assert 'Registration' in res.text
        assert 'Test Server | Welcome!' not in res.text
        assert res.status_code == 400, f"Got status code {res.status_code}, expected 400"

    @pytest.mark.parametrize(
        'login, email, password, expected_result',
        [
            (None, EXISTING_EMAIL, None, (409, 'User already exists')),
            (EXISTING_USERNAME, None, None, (409, 'User already exists')),
            (None, None, EXISTING_PASSWORD, (200, 'Logged as')),
        ],
        ids=['existing_email', 'existing_username', 'existing_pass']
    )
    @pytest.mark.API
    def test_api_create_existing_user(self, login, email, password, expected_result):
        """
        Тест на попытку зарегистрировать пользователя с данными уже существующего пользователя

        :param login
        :param email
        :param password
        :param expected_result
        Ожидаемый статус код содержится в expected_result
        """
        if login == EXISTING_USERNAME:
            login = self.base_user.username
        if password == EXISTING_PASSWORD:
            password = self.base_user.password
        if email == EXISTING_EMAIL:
            email = self.base_user.email
        self.user, res = self.api_client.post_register(login, email, password)
        assert res.status_code == expected_result[0], \
            f"Got status code {res.status_code}, expected {expected_result[0]}"
        assert expected_result[1] in res.text


