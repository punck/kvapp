from flask import Flask, request, jsonify, make_response
import dbm
import jwt
from functools import wraps
import datetime


class KVServer:
    def __init__(self):
        self._app = None

        # implement kvstore
        self._store = dbm.open('kv_store', 'c')

    def _token_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):

            token = None

            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']

            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = jwt.decode(
                    token,
                    self._app.config['S3CR3T_KEY'],
                    'HS256')

                current_user = data['user']
            except:
                return jsonify({'message': 'token is invalid'})

            return f(current_user, *args, **kwargs)

        return decorator

    def _insert(self, key, value):
        try:
            self._store[key] = value

        except dbm.error as e:
            raise e

    def _value_to_key(self, key):
        ekey = key.encode('utf-8')

        if ekey not in self._store.keys():
            return False, None
        else:
            return True, self._store[ekey].decode('utf-8')

    def _key_to_value(self, value):
        return True, ['keys']

    def start(self):
        self._app = Flask(__name__)
        self._app.config['S3CR3T_KEY'] = 'chupachups'

        @self._app.route('/login', methods=['GET', 'POST'])
        def login():
            token = jwt.encode(
                {'user': 'punck', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                self._app.config['S3CR3T_KEY'],
                algorithm="HS256"
            )
            return jsonify({'token': token})

        @self._app.route('/search', methods=['GET'])
        @self._token_required
        def search(current_user):

            if request.json.get('key'):
                key = request.json.get('key')

                # get values from store
                found, val = self._value_to_key(key)
                if found:
                    return make_response(jsonify({'key': key, 'value': val}), 200)
                else:
                    return make_response('', 204)

            if request.json.get('value'):
                value = request.json.get('value')

                # get keys from store
                found, keys = self._key_to_value(value)
                if found:
                    return make_response(jsonify({'value': value, 'keys': keys}), 200)
                else:
                    return make_response('', 204)

                return make_response(jsonify(d), 200)

            # default msg
            return make_response(jsonify({'msg': 'undefined parameter settings'}), 400)

        @self._app.route('/insert', methods=['POST'])
        @self._token_required
        def insert():
            key = request.json.get('key')
            value = request.json.get('value')

            try:
                self._insert(key, value)
                return make_response(jsonify({'key': key, 'value': value}), 201)
            except dbm.error:
                return make_response('', 500)

        self._app.run()
