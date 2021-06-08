import os

from flask import Flask, jsonify


app = Flask(__name__)

SURNAME_DATA = {}
user_id_seq = 1


class RoutesForMock:

    @staticmethod
    @app.route('/vk_id/<name>', methods=['GET'])
    def get_user_surname(name):
        if name:
            return jsonify({'vk_id': ('id' + name.replace(' ', ''))}), 200
        else:
            return jsonify(f'ID for user {name} not found'), 404


if __name__ == '__main__':
    host = os.environ.get('STUB_HOST', '0.0.0.0')
    port = os.environ.get('STUB_PORT', '8090')

    app.run(host, port)
