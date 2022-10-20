"""Test the handling of PUT requests"""

import json

from bookappbackend.tests.helpers import send_text, receive_text, get_sock

def test_put_invalid():
    """Test invalid put requests"""
    data = [({
            "request": "PUT",
            "data": {}
        }, "Missing key 'type' in request "),
        ({
            "request": "PUT",
            "type": "",
        }, "Missing key 'data' in request ")
    ]
    for request, error in data:
        # create a socket connection
        sock = get_sock()
        # send the request
        send_text(sock, json.dumps(request))

        # get back an answer
        recv_message = receive_text(sock)
        recv_dict: dict = json.loads(recv_message)

        assert recv_dict["error"]
        assert recv_dict["data"] == f"{error}{json.dumps(request)}".replace('"', "'")

def test_put_book(sock):
    """Test adding a book using a PUT request"""

    data = {
        "request": "PUT",
        "type": "book",
        "data": {
            "title": "Schachnovelle",
            "author": "Stefan Zweig"
        }
    }
    send_text(sock, json.dumps(data))

    recv_message = receive_text(sock)
    recv_dict: dict = json.loads(recv_message)
    assert not recv_dict["error"]

def test_put_book_invalid():
    """Test invalid put requests for books"""

    data = [({
            "request": "PUT",
            "type": "book",
            "data": {
                "title": "Schachnovelle",
            }
        }, "Missing key 'author' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "data": {
                "author": "Stefan Zweig"
            }
        }, "Missing key 'title' in request ")
    ]

    for request, error in data:
        # create a socket connection
        sock = get_sock()
        # send the request
        send_text(sock, json.dumps(request))

        # get back an answer
        recv_message = receive_text(sock)
        recv_dict: dict = json.loads(recv_message)

        assert recv_dict["error"]
        assert recv_dict["data"] == f"{error}{json.dumps(request)}".replace('"', "'")

def test_put_user(sock):
    """Test adding a user using a PUT request"""

    data = {
        "request": "PUT",
        "type": "user",
        "data": {
            "email": "pfeiff123456@imag.mail.com",
            "pw_hash": "abcde"
        }
    }
    send_text(sock, json.dumps(data))

    recv_message = receive_text(sock)
    recv_dict: dict = json.loads(recv_message)
    assert not recv_dict["error"]

def test_put_user_invalid():
    """Test invalid put requests for users"""

    data = [({
            "request": "PUT",
            "type": "user",
            "data": {
                "pw_hash": "abcde"
            }
        }, "Missing key 'email' in request "),
        ({
            "request": "PUT",
            "type": "user",
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
        recv_dict: dict = json.loads(recv_message)

        assert recv_dict["error"]
        assert recv_dict["data"] == f"{error}{json.dumps(request)}".replace('"', "'")
