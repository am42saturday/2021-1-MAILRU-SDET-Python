import json
import threading

from flask import Flask, jsonify, request

from hw7 import settings

app = Flask(__name__)

DATA = [[1, 'Alyx', 'Vance'],
        [2, 'Ivan', 'Egorov'],
        [3, 'Johnny', 'Silverhand']]

user_id_seq = 1


@app.route('/get_user/<name>', methods=['GET'])
def get_user(name):
    for user in DATA:
        if name in user:
            return jsonify(user[0], user[1], user[2]), 200
    else:
        return jsonify(f'User {name} not found'), 404


@app.route('/add_user', methods=['POST'])
def create_user():
    global user_id_seq

    user: dict = json.loads(request.data)
    name = user['name']
    surename = user.get('surename')

    for user in DATA:
        if name in user:
            return jsonify(f'User name {name} already exists'), 400

    DATA.append([user_id_seq, name, surename])

    user_id_seq += 1
    return jsonify(f'User {name} successfully created'), 201


@app.route('/edit_user/<name>', methods=['PUT'])
def edit_user(name):
    user: dict = json.loads(request.data)
    new_name = user['name']
    new_surename = user.get('surename')

    for user in DATA:
        if name in user:
            user[1] = new_name
            user[2] = new_surename
            return jsonify(f'User {name} successfully edited'), 201

    return jsonify(f'User name {name} does not exist'), 400


@app.route('/delete_user/<name>', methods=['DELETE'])
def delete_user(name):
    for user in DATA:
        if name in user:
            DATA.remove(user)
            return jsonify({"status": "Ok"}), 200
    else:
        return jsonify(f'User {name} not found and not deleted'), 404


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify(f'OK, exiting'), 200