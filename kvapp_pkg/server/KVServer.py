from flask import Flask, request, jsonify, make_response
import dbm
import jwt
from functools import wraps
import datetime
import os
import signal


class Config(object):
    DEBUG = False
    TESTING = False
    STORE_PATH = 'kv_store'
    S3CR3T_K3Y = 'chupachups'
    # If not set and the request does not specify a CONTENT_LENGTH, no data will be read for security.
    MAX_CONTENT_LENGTH = 1024 * 1024


class DevelopmentConfig(Config):
    DEBUG = True


class KVServer:
    def __init__(self, **kwargs):
        self._app = Flask(__name__)
        self._app.config.from_object(DevelopmentConfig())

        if 'path' in kwargs:
            self._app.config['STORE_PATH'] = kwargs['path']

        self._store = dbm.open(self._app.config['STORE_PATH'], 'c')

        @self._app.route('/api/auth', methods=['GET', 'POST'])
        def authorize():
            token = jwt.encode(
                {'user': 'punck', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                self._app.config['S3CR3T_K3Y'],
                algorithm="HS256"
            )
            return jsonify({'token': token})

        @self._app.route('/api/search', methods=['GET'])
        @self._token_required
        def search(current_user):
            if not len(request.json) == 1 or ('key' not in request.json and 'prefix' not in request.json):
                return make_response(jsonify({'msg': 'undefined parameter settings'}), 400)

            if request.json.get('key'):
                key = request.json.get('key')

                # get values from store
                found, val = self._value_to_key(key)
                if found:
                    return make_response(jsonify({'key': key, 'value': val}), 200)
                else:
                    return make_response('', 204)

            if request.json.get('prefix'):
                value = request.json.get('prefix')

                # get keys from store
                found, keys = self._key_to_value(value)
                if found:
                    return make_response(jsonify({'prefix': value, 'result': keys}), 200)
                else:
                    return make_response('', 204)

            # default msg
            return make_response(jsonify({'msg': 'undefined parameter settings'}), 400)

        @self._app.route('/api/insert', methods=['POST'])
        @self._token_required
        def insert(current_user):

            if not len(request.json) == 2 or 'key' not in request.json or 'value' not in request.json:
                return make_response(jsonify({'msg': 'undefined parameter settings'}), 400)

            key = request.json.get('key')
            value = request.json.get('value')

            # TODO: process value

            try:
                self._insert(key, value)
                return make_response(jsonify({'key': key, 'value': value}), 201)
            except dbm.error:
                return make_response('', 500)

    def get_app(self):
        return self._app

    def _insert(self, key, value):
        try:
            self._store[key] = value

        except dbm.error as e:
            raise e

    def _value_to_key(self, key):
        ekey = key.encode('utf-8')

        if ekey not in self._store.keys():
            return False, None

        return True, self._store[ekey].decode('utf-8')

    def _key_to_value(self, prefix):

        if not any(v.decode('utf-8').startswith(prefix) for v in self._store.values()):
            return False, None

        res = [{'key': k.decode('utf-8'), 'value': v.decode('utf-8')} for k, v in self._store.items() if v.decode('utf-8').startswith(prefix)]

        return True, res

    def _token_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):

            token = request.headers['x-access-tokens']  if 'x-access-tokens' in request.headers else None

            if not token:
                return jsonify({'msg': 'token is missing'})

            try:
                data = jwt.decode(
                    token,
                    self._app.config['S3CR3T_K3Y'],
                    'HS256')

                current_user = data['user']
            except:
                return jsonify({'msg': 'token is invalid'})

            return f(current_user, *args, **kwargs)

        return decorator

    def start(self):
        self._app.run()
