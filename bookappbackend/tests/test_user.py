"""Test user related requests"""

import json
import pytest
import bcrypt

import bookappbackend.tests.fixtures as fixtures
from bookappbackend.tests.helpers import send_text, receive_text, get_sock, assert_response

@pytest.mark.order(0)
def test_user_creation(pytestuser):
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(pytestuser["password"].encode("utf8"), salt)

    request = {
        "request": "PUT",
        "type": "user",
        "data": {
            "email": pytestuser["email"],
            "pw_hash": pw_hash.decode("utf8"),
            "salt": salt.decode("utf8")
        }
    }
    sock = get_sock()
    send_text(sock, json.dumps(request))

    response = receive_text(sock)
    assert_response(response)

    request = {
        "request": "GET",
        "type": "salt",
        "data": {
            "email": pytestuser["email"]
        }
    }
    sock = get_sock()
    send_text(sock, json.dumps(request))

    response = receive_text(sock)
    assert json.loads(response)["data"]["salt"] == salt.decode("utf8")
    assert_response(response, [("salt", str, salt.decode("utf8"))])

    fixtures.salt = salt

@pytest.mark.order(1)
def test_user_login(pytestuser):
    pw_hash = bcrypt.hashpw(pytestuser["password"].encode("utf8"), pytestuser["salt"])

    request = {
        "request": "GET",
        "type": "token",
        "auth": {
            "type": "password",
            "email": pytestuser["email"],
            "pw_hash": pw_hash.decode("utf8")
        }
    }
    sock = get_sock()
    send_text(sock, json.dumps(request))

    response = receive_text(sock)
    assert_response(response, [("token", str, None)])
    token = json.loads(response)["data"]["token"]

    request = {
        "request": "GET",
        "type": "user",
        "auth": {
            "type": "token",
            "token": token
        }
    }
    sock = get_sock()
    send_text(sock, json.dumps(request))

    response = receive_text(sock)
    assert_response(response, [("user_id", int, None), ("email", str, pytestuser["email"]), ("borrows", list, None)])

    fixtures.token = token

@pytest.mark.order(5)
def test_put_user_invalid(pytestuser):
    """Test invalid put requests for users"""

    data = [({
            "request": "PUT",
            "type": "user",
            "auth": {
                "type": "token",
                "token": pytestuser["token"]
            },
            "data": {
                "pw_hash": "abcde"
            }
        }, "Missing key 'email' in request "),
        ({
            "request": "PUT",
            "type": "user",
            "auth": {
                "type": "token",
                "token": pytestuser["token"]
            },
            "data": {
                "email": "pfeiff123456@imag.mail.com",
            }
        }, "Missing key 'pw_hash' in request ")
    ]

    for request, error in data:
        # create a socket connection
        sock = get_sock()
        # send the request
        send_text(sock, json.dumps(request))

        # get back an answer
        recv_message = receive_text(sock)
        try:
            recv_dict = json.loads(recv_message)
        except json.JSONDecodeError:
            raise Exception(f"{recv_message}")

        assert recv_dict["error"], f"{recv_dict['data']}"
        assert recv_dict["data"] == f"{error}{json.dumps(request)}".replace('"', "'")

@pytest.mark.order(6)
def test_get_user_invalid(pytestuser):
    """Test invalid get requests for users"""

    data = [({
            "request": "GET",
            "type": "user",
            "auth": {
                "token": pytestuser["token"]
            }
        }, "Missing key 'type' in request "),
        ({
            "request": "GET",
            "type": "user",
            "auth": {
                "type": "token"
            }
        }, "Missing key 'token' in request "),
    ]

    for request, error in data:
        # create a socket connection
        sock = get_sock()
        # send the request
        send_text(sock, json.dumps(request))

        # get back an answer
        recv_message = receive_text(sock)
        try:
            recv_dict = json.loads(recv_message)
        except json.JSONDecodeError:
            raise Exception(f"{recv_message}")

        assert recv_dict["error"], f"{recv_dict['data']}"
        assert recv_dict["data"] == f"{error}{json.dumps(request)}".replace('"', "'")
