import json

from hw7 import settings
from hw7.client.client import HttpClient

url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'


class TestMock:

    def test_get_existing_user(self):
        client = HttpClient()
        res = client.get('/get_user/Alyx')

        assert res[0] == 'HTTP/1.0 200 OK'
        assert json.loads(res[-1])[1] == "Alyx"

    def test_get_not_existing_user(self):
        client = HttpClient()
        res = client.get('/get_user/guwafou')

        assert res[0] == 'HTTP/1.0 404 NOT FOUND'
        assert json.loads(res[-1]) == "User guwafou not found"

    def test_delete_existing_user(self):
        client = HttpClient()
        res = client.get('/get_user/Ivan')
        assert res[0] == 'HTTP/1.0 200 OK'
        assert json.loads(res[-1])[1] == "Ivan"

        client = HttpClient()
        data = client.delete('/delete_user/Ivan')
        assert data[0] == 'HTTP/1.0 200 OK'
        assert json.loads(data[-1])["status"] == "Ok"

        client = HttpClient()
        res = client.get('/get_user/Ivan')
        assert res[0] == 'HTTP/1.0 404 NOT FOUND'
        assert json.loads(res[-1]) == "User Ivan not found"

    def test_delete_not_existing_user(self):
        client = HttpClient()
        res = client.get('/get_user/vhgweq')
        assert res[0] == 'HTTP/1.0 404 NOT FOUND'
        assert json.loads(res[-1]) == "User vhgweq not found"

        client = HttpClient()
        data = client.delete('/delete_user/vhgweq')
        assert data[0] == 'HTTP/1.0 404 NOT FOUND'
        assert json.loads(data[-1]) == "User vhgweq not found and not deleted"

    def test_edit_existing_user(self):
        client = HttpClient()
        res = client.get('/get_user/Johnny')
        assert res[0] == 'HTTP/1.0 200 OK'
        assert json.loads(res[-1])[1] == "Johnny"
        assert json.loads(res[-1])[2] == "Silverhand"

        client = HttpClient()
        data = client.put('/edit_user/Johnny', '{"name": "Johnny", "surename": "Ivanov"}')
        assert data[0] == 'HTTP/1.0 201 CREATED'
        assert json.loads(data[-1]) == "User Johnny successfully edited"

        client = HttpClient()
        res = client.get('/get_user/Johnny')
        assert res[0] == 'HTTP/1.0 200 OK'
        assert json.loads(res[-1])[1] == "Johnny"
        assert json.loads(res[-1])[2] == "Ivanov"

    def test_edit_not_existing_user(self):
        client = HttpClient()
        res = client.get('/get_user/dsafhjbkad')
        assert res[0] == 'HTTP/1.0 404 NOT FOUND'
        assert json.loads(res[-1]) == "User dsafhjbkad not found"

        client = HttpClient()
        data = client.put('/edit_user/dsafhjbkad', '{"name": "dsafhjbkad", "surename": "gdaudjd"}')
        assert data[0] == 'HTTP/1.0 400 BAD REQUEST'
        assert json.loads(data[-1]) == "User name dsafhjbkad does not exist"

        client = HttpClient()
        res = client.get('/get_user/dsafhjbkad')
        assert res[0] == 'HTTP/1.0 404 NOT FOUND'
        assert json.loads(res[-1]) == "User dsafhjbkad not found"

    def test_create_user(self):
        client = HttpClient()
        res = client.get('/get_user/Sam')
        assert res[0] == 'HTTP/1.0 404 NOT FOUND'
        assert json.loads(res[-1]) == "User Sam not found"

        client = HttpClient()
        client.post('/add_user', '{"name": "Sam", "surename": "Bridges"}')

        client = HttpClient()
        res = client.get('/get_user/Sam')

        assert res[0] == 'HTTP/1.0 200 OK'
        assert json.loads(res[-1])[1] == "Sam"
        assert json.loads(res[-1])[2] == "Bridges"

    def test_create_existing_user(self):
        client = HttpClient()

        res = client.get('/get_user/Alyx')
        assert res[0] == 'HTTP/1.0 200 OK'
        assert json.loads(res[-1])[1] == 'Alyx'

        client = HttpClient()

        data = client.post('/add_user', '{"name": "Alyx", "surename": "Vance"}')
        assert data[0] == "HTTP/1.0 400 BAD REQUEST"
        assert json.loads(data[-1]) == "User name Alyx already exists"

        client = HttpClient()

        res = client.get('/get_user/Alyx')

        assert res[0] == 'HTTP/1.0 200 OK'
        assert json.loads(res[-1])[1] == 'Alyx'

    def test_create_user_without_surename(self):
        client = HttpClient()

        res = client.get('/get_user/Paul')
        assert res[0] == 'HTTP/1.0 404 NOT FOUND'
        assert json.loads(res[-1]) == "User Paul not found"
        client = HttpClient()
        client.post('/add_user', '{"name": "Paul"}')
        client = HttpClient()
        res = client.get('/get_user/Paul')

        assert res[0] == 'HTTP/1.0 200 OK'
        assert json.loads(res[-1])[1] == "Paul"

