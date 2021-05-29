import json
import logging
import socket

from hw7 import settings

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 100


class HttpClient:
    host = settings.MOCK_HOST
    port = int(settings.MOCK_PORT)

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(settings.TIMEOUT)
        self.client.connect((self.host, self.port))

    @staticmethod
    def log_pre(request):
        logger.info(f'\nREQUEST:\n{request}')

    @staticmethod
    def log_post(response):
        logger.info(f'\nRESPONSE:\n{response[0]}\n'
                    f'{response[1]}\n'
                    f'{response[2]}\n'
                    f'{response[3]}\n'
                    f'{response[4]}\n'
                    f'{response[5]}\n'
                    f'{response[6]}'
                    )

    def post(self, params, data):
        json_data = json.dumps(data)
        res_data = json.loads(json_data)

        request = f'POST {params} HTTP/1.1\r\n' \
                  f'Host: {self.host}\r\n' \
                  f'Content-Length: {len(res_data)}\r\n' \
                  f'Content-Type: application/json\r\n\r\n' \
                  f'{res_data}\r\n\r\n'
        self.log_pre(request)

        self.client.send(request.encode())
        response = self.get_response_data(self.client)
        self.log_post(response)

        return response

    def get(self, params):
        request = f'GET {params} HTTP/1.1\r\n' \
                  f'Host:{self.host}:{self.port}\r\n\r\n'
        self.log_pre(request)

        self.client.send(request.encode())
        response = self.get_response_data(self.client)
        self.log_post(response)

        return response

    def put(self, params, data):
        json_data = json.dumps(data)
        res_data = json.loads(json_data)

        request = f'PUT {params} HTTP/1.1\r\n' \
                  f'Host: {self.host}\r\n' \
                  f'Content-Length: {len(res_data)}\r\n' \
                  f'Content-Type: application/json\r\n\r\n' \
                  f'{res_data}\r\n\r\n'
        self.log_pre(request)

        self.client.send(request.encode())
        response = self.get_response_data(self.client)
        self.log_post(response)

        return response

    def delete(self, params):
        request = f'DELETE {params} HTTP/1.1\r\n' \
                  f'Host: {self.host}:{self.port}\r\n\r\n'
        self.log_pre(request)

        self.client.send(request.encode())
        response = self.get_response_data(self.client)
        self.log_post(response)

        return response

    @staticmethod
    def get_response_data(client):
        total_data = []

        while True:
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                client.close()
                break

        data = ''.join(total_data).splitlines()

        return data

