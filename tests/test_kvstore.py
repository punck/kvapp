import kvapp_pkg.server.KVServer as kvs


def test_insert():
    """
    Test insert to kvstore
    """
    server = kvs.KVServer()
    rv = server._insert('key', 'value')

    assert rv is None

def test_search_good_key():
    """
    Test search by key with existing key
    """
    server = kvs.KVServer()
    rv = server._value_to_key('key')

    assert rv == (True, 'value')

def test_search_bad_key():
    """
    Test search by key with non-existing key
    """
    server = kvs.KVServer()
    rv = server._value_to_key('key2')

    assert rv == (False, None)


def test_search_good_value():
    """
    Test search by value with existing prefix
    """
    server = kvs.KVServer()
    rv = server._key_to_value('val')

    assert rv == (True, [{'key': 'key', 'value': 'value'}])


def test_search_bad_value():
    """
    Test search by value with non-existing prefix
    """
    server = kvs.KVServer()
    rv = server._key_to_value('val2')

    assert rv == (False, None)


