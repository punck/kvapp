import kvapp_pkg.KVServer as kvs
import pytest

pytest.token = None

def test_auth():
    """
    Test if a token is returned
    """

    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/auth')

    assert response.status_code == 200
    assert 'token' in response.get_json()
    pytest.token = response.get_json()['token']
    assert isinstance(pytest.token, str)


def test_insert_NOK_missing_token():
    """
    Test insert in case of a missing token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.post('/api/insert', json={'key': 'kulcs', 'value': 'érték'})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is missing'


def test_insert_NOK_missing_token_2():
    """
    Test insert in case of a missing token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.post('/api/insert', json={'key': 'kulcs', 'value': 'érték'}, headers={'x-access-tokens': ''})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is missing'


def test_insert_NOK_invalid_token():
    """
    Test insert in case of an invalid token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.post('/api/insert', json={'key': 'kulcs', 'value': 'érték'}, headers={'x-access-tokens': 'rossztok'})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is invalid'


def test_insert_NOK_undef_params():
    """
    Test insert with wrong parameters
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.post('/api/insert', json={'key': 'kulcs', 'value': 'érték', 'extra': 'extra'}, headers={'x-access-tokens': pytest.token})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'undefined parameter settings'


def test_insert_OK():
    """
    Test insert when everything is OK
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.post('/api/insert', json={'key': 'kulcs', 'value': 'érték'}, headers={'x-access-tokens': pytest.token})

    assert response.status_code == 201
    assert response.get_json() == {'key': 'kulcs', 'value': 'érték'}


def test_search_by_key_NOK_missing_token():
    """
    Test search by key in case of a missing token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'key': 'kulcs'})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is missing'


def test_search_by_key_NOK_missing_token_2():
    """
    Test search by key in case of a missing token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'key': 'kulcs'}, headers={'x-access-tokens': ''})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is missing'


def test_search_by_key_NOK_invalid_token():
    """
    Test search by key in case of an invalid token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'key': 'kulcs'}, headers={'x-access-tokens': 'rossztok'})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is invalid'


def test_search_by_key_NOK_undef_params():
    """
    Test search by key in case of wrong parameters
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'key': 'kulcs', 'ismeretlen': 'ism'}, headers={'x-access-tokens': pytest.token})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'undefined parameter settings'


def test_search_by_key_OK_no_result():
    """
    Test search by key with no result
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'key': 'kulcsa'}, headers={'x-access-tokens': pytest.token})

    assert response.status_code == 204
    assert response.get_json() is None


def test_search_by_key_OK():
    """
    Test search by key when everything is OK
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'key': 'kulcs'}, headers={'x-access-tokens': pytest.token})

    assert response.status_code == 200
    assert response.get_json() == {'key': 'kulcs', 'value': 'érték'}


# test_search_by_prefix OK, NOK

def test_search_by_prefix_NOK_missing_token():
    """
    Test search by prefix in case of a missing token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'prefix': 'ért'})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is missing'


def test_search_by_prefix_NOK_missing_token_2():
    """
    Test search by prefix in case of a missing token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'prefix': 'ért'}, headers={'x-access-tokens': ''})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is missing'


def test_search_by_prefix_NOK_invalid_token():
    """
    Test search by prefix in case of an invalid token
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'prefix': 'ért'}, headers={'x-access-tokens': 'rossztok'})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'token is invalid'


def test_search_by_prefix_NOK_undef_params():
    """
    Test search by prefix in case of wrong parameters
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'prefix': 'ért', 'ismeretlen': 'ism'}, headers={'x-access-tokens': pytest.token})

    assert response.status_code == 400
    assert response.get_json()['msg'] == 'undefined parameter settings'


def test_search_by_prefix_OK_no_result():
    """
    Test search by prefix with no result
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'prefix': 'nincs'}, headers={'x-access-tokens': pytest.token})

    assert response.status_code == 204
    assert response.get_json() is None


def test_search_by_prefix_OK():
    """
    Test search by prefix when everything is OK
    """
    server = kvs.KVServer()
    app = server.get_app()

    with app.test_client() as test_client:
        response = test_client.get('/api/search', json={'prefix': 'ért'}, headers={'x-access-tokens': pytest.token})

    assert response.status_code == 200
    assert response.get_json() == {'prefix': 'ért', 'result': [{'key': 'kulcs', 'value': 'érték'}]}