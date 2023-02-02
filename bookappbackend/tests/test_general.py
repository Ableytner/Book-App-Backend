"""Test general requests"""

import json
import pytest

from bookappbackend.tests.helpers import send_text, receive_text, get_sock

@pytest.mark.order(5)
def test_invalid_general():
    """Test invalid requests"""
    data = [({
        }, "Missing key 'request' in request "),
        ({
            "request": ""
        }, "Invalid value '' for key 'request' in request "),
        ({
            "request": "GET",
        }, "Missing key 'type' in request "),
        ({
            "request": "GET",
            "type": "",
        }, "Invalid value '' for key 'type' in request "),
        ({
            "request": "PUT",
            "type": "book",
        }, "Missing key 'data' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "data": {}
        }, "Missing key 'auth' in request ")
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

@pytest.mark.order(5)
def test_invalid_auth(pytestuser):
    """Test invalid requests"""
    data = [({
            "request": "PUT",
            "type": "book",
            "auth": {},
            "data": {}
        }, "Missing key 'type' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": ""
            },
            "data": {}
        }, "Invalid value '' for key 'type' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": "token"
            },
            "data": {}
        }, "Missing key 'token' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": "token",
                "token": ""
            },
            "data": {}
        }, "Invalid value '' for key 'token' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": "password"
            },
            "data": {}
        }, "Missing key 'email' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": "password",
                "email": ""
            },
            "data": {}
        }, "Invalid value '' for key 'email' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": "password",
                "email": pytestuser["email"]
            },
            "data": {}
        }, "Missing key 'pw_hash' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": "password",
                "email": pytestuser["email"],
                "pw_hash": ""
            },
            "data": {}
        }, "Invalid value '' for key 'pw_hash' in request ")
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

@pytest.mark.order(5)
def test_corrupted():
    """Test a corrupted request"""

    data = {
        "request": "GET",
        "type": "",
        "data": {}
    }
    data_corrs = [
        f"asdf{json.dumps(data)}asdf",
        f"wasd{json.dumps(data)}",
        f"{json.dumps(data)}dsaw",
        f"{json.dumps(data).replace('{', '(')}",
        f"{json.dumps(data).replace('}', ')')}",
        f"{json.dumps(data).replace(',', ';')}"
    ]
    error_msg = "Could not decode request "

    for data_corr in data_corrs:
        sock = get_sock()
        send_text(sock, data_corr)

        recv_message = receive_text(sock)
        try:
            recv_dict = json.loads(recv_message)
        except json.JSONDecodeError:
            raise Exception(f"{recv_message}")
        assert recv_dict["error"], f"{recv_dict['data']}"
        assert recv_dict["data"] == f"{error_msg}{data_corr}"
