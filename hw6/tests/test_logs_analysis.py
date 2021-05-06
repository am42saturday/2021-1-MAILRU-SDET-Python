import os
import re
import pytest
from itertools import islice

from hw6.mysql.builder import MySQLBuilder
from hw6.mysql.models import AllRequests, RequestsByMethod, Top10FrequentRequest, Top5Largest4xxRequests, \
    Top5Users5xxRequests
from hw6.utils.nginx_parser import lineformat


class MySQLBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)

        self.prepare()


class TestRequestsQuantity(MySQLBase):

    def prepare(self):
        with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
            count = 0
            for _ in logs.readlines():
                count += 1
        self.mysql_builder.create_all_requests_record("Общее количество запросов", count)

    def test_number_of_requests(self):
        # get data from db
        all_requests = self.mysql.session.query(AllRequests).all()

        # check data
        assert len(all_requests) == 1
        for record in all_requests:
            assert record.quantity == 225133


class TestRequestsQuantityByMethod(MySQLBase):

    def prepare(self):
        result_data = []
        with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
            for line in logs.readlines():
                data = re.search(lineformat, line)
                if data:
                    datadict = data.groupdict()
                    method = datadict["method"]
                    result_data.append(method)

        counts = dict()
        for i in result_data:
            counts[i] = counts.get(i, 0) + 1

        for method, number in counts.items():
            self.mysql_builder.create_requests_by_method_record(method, number)

    def test_requests_by_method(self):
        # get data from db
        requests_by_method = self.mysql.session.query(RequestsByMethod).all()

        # check data
        assert len(requests_by_method) == 5
        correct_results_method = [('POST', 102503),
                                  ('GET', 122095),
                                  ('HEAD', 528),
                                  ('PUT', 6),
                                  ('g369g=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B&z0=QGluaV9zZXQoI'
                                   'mRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc1'
                                   '9ydW50aW1lKDApO2VjaG8oIi0%2bfCIpOztlY2hvKCJlNTBiNWYyYjRmNjc1NGFmMDljYzg0NWI4Y'
                                   'jU4ZTA3NiIpOztlY2hvKCJ8PC0iKTs7ZGllKCk7GET', 1)]
        for record in requests_by_method:
            assert record.method == correct_results_method[record.id - 1][0]
            assert record.quantity == correct_results_method[record.id - 1][1]


class TestTop10FrequentRequests(MySQLBase):

    def prepare(self):
        result_data = []
        with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
            for line in logs.readlines():
                data = re.search(lineformat, line)
                datadict = data.groupdict()
                if data:
                    url = datadict["url"]
                    result_data.append(url)

        counts = dict()
        for i in result_data:
            counts[i] = counts.get(i, 0) + 1
        sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

        for url, number in islice(sorted_counts.items(), 10):
            self.mysql_builder.create_top_10_frequent_requests_record(url, number)

    def test_top_10_frequent_requests(self):
        # get data from db
        top_10_frequent_requests = self.mysql.session.query(Top10FrequentRequest).all()

        # check data
        assert len(top_10_frequent_requests) == 10
        correct_results = [
            '/administrator/index.php ',
            '/apache-log/access.log ',
            '/ ',
            '/templates/_system/css/general.css ',
            '/robots.txt ',
            'http://almhuette-raith.at/administrator/index.php ',
            '/favicon.ico ',
            '/wp-login.php ',
            '/administrator/ ',
            '/templates/jp_hotel/css/template.css ']
        for record in top_10_frequent_requests:
            assert record.url == correct_results[record.id - 1]


class TestTop5Largest4xxRequests(MySQLBase):

    def prepare(self):
        result_data = []
        with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
            for line in logs.readlines():
                data = re.search(lineformat, line)
                datadict = data.groupdict()
                pattern = re.compile(r'4..')
                if data and pattern.search(datadict["statuscode"]):
                    ip = datadict["ipaddress"]
                    url = datadict["url"]
                    bytessent = datadict["bytessent"]
                    status = datadict["statuscode"]
                    result_data.append([url, status, bytessent, ip])

        sorted_result = sorted(result_data, key=lambda elem: int(elem[2]), reverse=True)[:5]
        for record in sorted_result:
            self.mysql_builder.create_top_5_largest_4xx_requests_record(record[0], record[1], record[2], record[3])

    def test_top_5_largest_4xx_requests(self):
        # get data from db
        top_5_largest_4xx_requests = self.mysql.session.query(Top5Largest4xxRequests).all()

        # check data
        assert len(top_5_largest_4xx_requests) == 5
        pattern = re.compile(r'4..')
        correct_results = ['/index.php?option=com_phocagallery&view=category&id=4025&Itemid=53 ',
                           '/index.php?option=com_phocagallery&view=category&id=7806&Itemid=53 ',
                           '/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%289168%3'
                           'D4696%29%20THEN%209168%20ELSE%209168%2A%28SELECT%209168%20FROM%20INFORMATION_SCHEMA.'
                           'CHARACTER_SETS%29%20END%29%29&Itemid=53 ',
                           '/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%281753%3'
                           'D1753%29%20THEN%201753%20ELSE%201753%2A%28SELECT%201753%20FROM%20INFORMATION_SCHEMA.'
                           'CHARACTER_SETS%29%20END%29%29&Itemid=53 ',
                           '/index.php?option=com_easyblog&view=dashboard&layout=write '
                           ]
        for record in top_5_largest_4xx_requests:
            assert pattern.search(record.status_code)
            assert record.url == correct_results[record.id - 1]


class TestTop5Users5xxRequests(MySQLBase):

    def prepare(self):
        result_data = []
        with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
            for line in logs.readlines():
                data = re.search(lineformat, line)
                datadict = data.groupdict()
                pattern = re.compile(r'5..')
                if data and pattern.search(datadict["statuscode"]):
                    ip = datadict["ipaddress"]
                    result_data.append(ip)

        counts = dict()
        for i in result_data:
            counts[i] = counts.get(i, 0) + 1
        sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

        for ip, number in islice(sorted_counts.items(), 5):
            self.mysql_builder.create_top_5_users_5xx_request_record(ip, number)

    def test_top_5_users_5xx_requests(self):
        # get data from db
        top_5_users_5xx_requests = self.mysql.session.query(Top5Users5xxRequests).all()

        # check data
        assert len(top_5_users_5xx_requests) == 5
        correct_results_count = [225, 4, 3, 2, 2]
        correct_results_ip = ['189.217.45.73',
                              '82.193.127.15',
                              '91.210.145.36',
                              '194.87.237.6',
                              '198.38.94.207']
        for record in top_5_users_5xx_requests:
            assert record.quantity == correct_results_count[record.id-1]
            assert record.ip == correct_results_ip[record.id - 1]


