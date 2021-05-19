import json
import os

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app_data = {}
user_id_seq = 1


@app.route('/add_user', methods=['POST'])
def create_user():
    global user_id_seq

    user_name = json.loads(request.data)['name']
    if user_name not in app_data:
        app_data[user_name] = user_id_seq

        data = {'user_id': user_id_seq}
        user_id_seq += 1
        return jsonify(data), 201
    else:
        return jsonify(f'User name {user_name} already exists: if {app_data[user_name]}'), 400


@app.route('/get_user/<name>', methods=['GET'])
def get_user_id_by_name(name):
    if user_id := app_data.get(name):
        stub_host = os.environ['STUB_HOST']
        stub_port = os.environ['STUB_PORT']

        age = None
        try:
            age = requests.get(f'http://{stub_host}:{stub_port}/get_age/{name}').json()
        except Exception as e:
            print(f'Unable to get age from external system:\n{e}')

        mock_host = os.environ['MOCK_HOST']
        mock_port = os.environ['MOCK_PORT']

        surname = None
        try:
            resp = requests.get(f'http://{mock_host}:{mock_port}/get_surname/{name}')
            if resp.status_code == 200:
                surname = resp.json()

        except Exception as e:
            print(f'Unable to get surname from external system:\n{e}')

        data = {'user_id': user_id,
                'age': age,
                'surname': surname
                }

        return jsonify(data), 200
    else:
        return jsonify(f'User name {name} not found'), 404


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '8080')

    app.run(host, port)