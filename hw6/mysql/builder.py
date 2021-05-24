from faker import Faker

from hw6.mysql.models import AllRequests, RequestsByMethod, Top10FrequentRequest, Top5Largest4xxRequests, \
    Top5Users5xxRequests

fake = Faker()


class MySQLBuilder:

    def __init__(self, client):
        self.client = client
        self.answer = None

    def create_all_requests_record(self, question=None, quantity=None):
        if question is None:
            question = 'No question given'

        if quantity is None:
            quantity = 0

        answer = AllRequests(
            question=question,
            quantity=quantity
        )
        self.client.session.add(answer)
        self.client.session.commit()
        return answer

    def create_requests_by_method_record(self, method, quantity):
        if method is None:
            method = '-'

        if quantity is None:
            quantity = 0

        answer = RequestsByMethod(
            method=method,
            quantity=quantity
        )
        self.client.session.add(answer)
        self.client.session.commit()
        return answer

    def create_top_10_frequent_requests_record(self, url, quantity):
        if url is None:
            url = '-'

        if quantity is None:
            quantity = 0

        answer = Top10FrequentRequest(
            url=url,
            quantity=quantity
        )
        self.client.session.add(answer)
        self.client.session.commit()
        return answer

    def create_top_5_largest_4xx_requests_record(self, url, status_code, size, ip):
        if ip is None:
            ip = '-'

        if url is None:
            url = '-'

        if size is None:
            size = 0

        if status_code is None:
            status_code = '-'

        answer = Top5Largest4xxRequests(
            ip=ip,
            url=url,
            size=size,
            status_code=status_code
        )
        self.client.session.add(answer)
        self.client.session.commit()
        return answer

    def create_top_5_users_5xx_request_record(self, ip, quantity):
        if ip is None:
            ip = '-'

        if quantity is None:
            quantity = 0

        answer = Top5Users5xxRequests(
            ip=ip,
            quantity=quantity
        )
        self.client.session.add(answer)
        self.client.session.commit()
        return answer


