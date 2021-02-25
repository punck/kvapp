# KVApp package

This repository contains a demo key-value server application written in Python using Flask and dbm.
Several endpoints have been defined to manipulate the underlying key-value store.

## Description

The KVServer app utilizes python dbm (dumb). dbm package in python provides a simple dictionary like interface of the form DBM (DataBase Manager) generally used in Unix operating system.

dbm stores data in simple key – value pair form like a dictionary which makes it easier to insert, edit and retrieve data from database. It stores data by the use of a single primary key (“key”) in fixed size blocks.

There are three types of sub modules in dbm package:
- dbm.gnu: GNU’s reinterpretation of dbm
- dbm.ndbm: Interface based on ndbm
- dbm.dumb: Portable DBM implementation

The dbm.dumb module provides a persistent dictionary-like interface which is written entirely in Python. Unlike other modules such as dbm.gnu no external library is required. As with other persistent mappings, the keys and values are always stored as bytes.

Python's dictionary implementation is really fast for key-value storage, but not persistent. 

sqlite3 is fast but not as fast as dbm (when we persist to a file). In case of a workload where keys and values are added and retrieved very often,
and they always str or bytes, dbm is a reasonable choice.

## Building

### Dependencies
Check *requirements.txt*.

**Note**: *setup.py* is not included so dependencies are not specified ahead.

### Building

Make sure you have the latest versions of PyPA's build installed:

```
python3 -m pip install --upgrade build
```

Now run this command where *pyproject.toml* is located:
```
python3 -m build
```

This command should output a lot of text and once completed should generate two files in the dist directory:
```
dist/
  kvapp-pkg-szekersz-0.0.1-py3-none-any.whl
  kvapp-pkg-szekersz-0.0.1.tar.gz
```

## Testing
Navigate to the folder where **/tests** is located and run the following command:
```
python3 -m pytest tests/
```

It will execute 5 unit tests which test the *kv_store* and 18 end-to-end tests which test the API endpoints.

## Functions

### Starting the server
Import the following package:

```
import kvapp_pkg.KVServer as kvs
```

After you imported the package, create an instance of the server and call its *start()* method.

```
server = kvs.KVServer()
server.start()
```

By default, it will start listening on port 5000.

**Note**: there is no *graceful stop* implemented (/api/shutdown endpoint has been removed).

### Communicating with the server

#### 1. Get authentication
Authentication is required for every other operation.

**Endpoint**

```
(hostname:port)/api/auth
```

A JSON response containing the JWT *token* will be returned (key=token).

```
response body
{
    "token": "dummy_token"
}
```

#### 2. Inserting a key-value pair
**Endpoint**

```
(hostname:port)/api/insert
```

The request header must contain the *x-access-tokens* key with *token* as value.
If the token is missing or invalid, the corresponding message with response code 400 is returned('msg':'token missing/invalid').

```
request header
{
    "x-access-tokens"   : "dummy_token"
}
```

The request body must contain *key* and *value* keys (no other key is accepted). Otherwise, response code 400 is returned.

```
request body
{
    "key"   : "dummy_key",
    "value" : "dummy_value"
}
```

On successful insertion, a JSON response containing the key and value is returned with response code 201.
Otherwise, response code 500 is returned.

*In this version, if an existing key is given, the value is overwritten.*

#### 3. Searching by key or by prefix
**Endpoint**

```
(hostname:port)/api/search
```

The request header must contain the *x-access-tokens* key with *token* as value.
If the token is missing or invalid, the corresponding message with response code 400 is returned ('msg':'token missing/invalid').

The request body must contain either *key* or *value* key (no other key is accepted). Otherwise, response code 400 is returned.

#### By key
The request body must contain the *key* key.

```
request body
{
    "key"   : "dummy_key"
}
```

If there is no value found, respond code 204 is returned. Otherwise, a JSON response containing the key and its value is returned with response code 200.

```
response body
{
    "key"   : "dummy_key",
    "value" : "dummy_value"
}
```

#### By prefix
The request body must contain the *prefix* key.

```
request body
{
    "prefix"   : "dummy"
}
```

If there are no keys found, respond code 204 is returned. Otherwise, a JSON response containing the prefix and a results list is returned with response code 200. The result list contains key-value pairs.

```
response body
{
    "prefix"   : "dummy",
    "result"   : [
                    {"key": "dummy_key_1", "value": "dummy_value_1"},
                    {"key": "dummy_key_2", "value": "dummy_value_2"}
                 ]
}
```