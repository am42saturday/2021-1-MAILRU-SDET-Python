import logging
import json
from urllib.parse import urljoin

import allure
import requests
from requests import Response


logger = logging.getLogger('test')

MAX_RESPONSE_LENGTH = 500


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

        self.csrf_token = None
        self.sessionid_gtp = None

    @staticmethod
    def log_pre(method, url, headers, data, expected_status):
        logger.info(f'Performing {method} request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'expected status: {expected_status}\n\n')

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

    def _request(self, method, url, headers=None, data=None, params=None, expected_status=200):
        self.log_pre(method, url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data, params=params)
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')
        return response

    @allure.step('Получение csrf-токена')
    def get_token(self) -> str:
        location = urljoin(self.base_url, '/csrf/')

        res = self._request('GET', location)

        headers = res.headers['set-cookie'].split(';')

        token_header = [h for h in headers if 'csrftoken' in h]
        if not token_header:
            raise Exception('CSRF token not found in main page headers')

        token_header = token_header[0]
        token = token_header.split('=')[-1]

        return token

    @allure.step('Авторизация')
    def post_login(self, user, password):
        location = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'

        headers = {
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/',
        }

        data = {
            'email': user,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/',
        }

        self._request('POST', location, headers=headers, data=data)

        csrftoken = self.get_token()
        location = urljoin(self.base_url, '/api/v2/user/session.json')

        params = {
            'fields': 'sudoers__language,sudoers__username,sudoers__lastname,sudoers__types,sudoers__firstname,'
                      'sudoers__additional_info,sudoers__additional_emails,sudoers__email_settings,sudoers__account,'
                      'sudoers__active_banners,sudoers__agency,sudoers__agency_username,sudoers__branch_username,'
                      'sudoers__branch,sudoers__email,sudoers__id,sudoers__mailings,'
                      'sudoers__available_mailings,sudoers__max_active_banners,sudoers__permissions,'
                      'sudoers__status,sudoers__currency,sudoers__info_currency,sudoers__partner,'
                      'sudoers__dmp,sudoers__notifications,sudoers__regions,sudoers__timezone,sudoers__country',
        }

        result: Response = self._request('GET', location, params=params)

        return result, csrftoken

    @allure.step('Открыть страницу Audiences')
    def open_segments(self):
        location = urljoin(self.base_url, '/segments/segments_list')

        headers = {
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-Requested-With': 'XMLHttpRequest'
        }

        params = {
            'fields': 'relations__object_type,relations__object_id,relations__params,relations__params__score,'
                      'relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags',
            'limit': 500,
        }

        self._request('GET', location, headers=headers, params=params)

    @allure.step('Создать сегмент')
    def create_segment(self, segment_name, csrftoken):
        location = urljoin(self.base_url, '/api/v2/remarketing/segments.json')

        headers = {'Referer': 'https://target.my.com/segments/segments_list/new/',
                   'X-CSRFToken': csrftoken}

        params = {
            'fields': 'relations__object_type,relations__object_id,relations__params,'
                      'relations__params__score,relations__id,relations_count,id,name,'
                      'pass_condition,created,campaign_ids,users,flags'
        }

        data = '{"name":"%s","pass_condition":1,"relations":' \
               '[{"object_type":"remarketing_player","params":{"type":"positive","left":365,"right":0}}],' \
               '"logicType":"or"}' % segment_name

        result: Response = self._request('POST', location, headers=headers, data=data, params=params)

        segment_id = json.loads(result.content)['id']

        return result, segment_id

    @allure.step('Удалить сегмент')
    def delete_segment(self, segment_id, csrftoken) -> Response:
        location = urljoin(self.base_url, '/api/v1/remarketing/mass_action/delete.json')

        headers = {'Referer': 'https://target.my.com/segments/segments_list',
                   'X-CSRFToken': csrftoken}

        data = '[{"source_id":%s,"source_type":"segment"}]' % segment_id

        result: Response = self._request('POST', location, headers=headers, data=data)

        return result

