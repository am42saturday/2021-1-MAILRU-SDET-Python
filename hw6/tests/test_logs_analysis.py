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
            self.count = 0
            for _ in logs.readlines():
                self.count += 1
        self.mysql_builder.create_all_requests_record("Общее количество запросов", self.count)

    def test_number_of_requests(self):
        # get data from db
        all_requests = self.mysql.session.query(AllRequests).all()

        # check data
        assert len(all_requests) == len([self.count])


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

        self.counts = dict()
        for i in result_data:
            self.counts[i] = self.counts.get(i, 0) + 1

        for method, number in self.counts.items():
            self.mysql_builder.create_requests_by_method_record(method, number)

    def test_requests_by_method(self):
        # get data from db
        requests_by_method = self.mysql.session.query(RequestsByMethod).all()

        # check data
        assert len(requests_by_method) == len(self.counts)


class TestTop10FrequentRequests(MySQLBase):
    required_length = 10

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

        for url, number in islice(sorted_counts.items(), self.required_length):
            self.mysql_builder.create_top_10_frequent_requests_record(url, number)

    def test_top_10_frequent_requests(self):
        # get data from db
        top_10_frequent_requests = self.mysql.session.query(Top10FrequentRequest).all()

        # check data
        assert len(top_10_frequent_requests) == self.required_length


class TestTop5Largest4xxRequests(MySQLBase):
    required_length = 5

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

        sorted_result = sorted(result_data, key=lambda elem: int(elem[2]), reverse=True)[:self.required_length]
        for record in sorted_result:
            self.mysql_builder.create_top_5_largest_4xx_requests_record(record[0], record[1], record[2], record[3])

    def test_top_5_largest_4xx_requests(self):
        # get data from db
        top_5_largest_4xx_requests = self.mysql.session.query(Top5Largest4xxRequests).all()

        # check data
        assert len(top_5_largest_4xx_requests) == self.required_length


class TestTop5Users5xxRequests(MySQLBase):
    required_length = 5

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

        for ip, number in islice(sorted_counts.items(), self.required_length):
            self.mysql_builder.create_top_5_users_5xx_request_record(ip, number)

    def test_top_5_users_5xx_requests(self):
        # get data from db
        top_5_users_5xx_requests = self.mysql.session.query(Top5Users5xxRequests).all()

        # check data
        assert len(top_5_users_5xx_requests) == self.required_length

