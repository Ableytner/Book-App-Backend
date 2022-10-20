"""Test the handling of GET requests"""

import json

from bookappbackend.tests.helpers import get_sock, send_text, receive_text

def test_get_invalid():
    """Test invalid get requests"""
    data = [({
            "request": "GET",
            "data": {}
        }, "Missing key 'type' in request "),
        ({
            "request": "PUT",
            "type": "book",
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

def test_get_book():
    """Test the GET request by creating a book and then requesting it"""

    # request the book creation
    sock = get_sock()

    data = {
        "request": "PUT",
        "type": "book",
        "data": {
            "title": "Schachnovelle",
            "author": "Stefan Zweig"
        }
    }
    send_text(sock, json.dumps(data))

    # get back the book_id
    recv_message = receive_text(sock)
    recv_dict: dict = json.loads(recv_message)
    assert not recv_dict["error"]

    # request the book data
    sock = get_sock()
    data = {
        "request": "GET",
        "type": "book",
        "data": {
            "book_id": recv_dict["data"]["book_id"]
        }
    }
    send_text(sock, json.dumps(data))

    # get back the book data
    recv_message = receive_text(sock)
    recv_dict: dict = json.loads(recv_message)
    assert not recv_dict["error"]
    assert recv_dict["data"]["author"] == "Stefan Zweig"
    assert recv_dict["data"]["title"] == "Schachnovelle"

def test_get_book_invalid():
    """Test invalid get requests for books"""

    data = [({
            "request": "GET",
            "type": "book",
            "data": {
            }
        }, "Missing key 'book_id' in request ")
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

def test_get_user():
    """Test the GET request by creating a user and then requesting it"""

    # request the book creation
    sock = get_sock()

    data = {
        "request": "PUT",
        "type": "user",
        "data": {
            "email": "pfeiff123456@imag.mail.com",
            "pw_hash": "abcde"
        }
    }
    send_text(sock, json.dumps(data))

    # get back the token
    recv_message = receive_text(sock)
    recv_dict: dict = json.loads(recv_message)
    assert not recv_dict["error"]

    # request the user data
    sock = get_sock()
    data = {
        "request": "GET",
        "type": "user",
        "data": {
            "auth_type": "password",
            "email": "pfeiff123456@imag.mail.com",
            "pw_hash": "abcde"
        }
    }
    send_text(sock, json.dumps(data))

    # get back the user data
    recv_message = receive_text(sock)
    recv_dict: dict = json.loads(recv_message)
    assert not recv_dict["error"]
    assert recv_dict["data"]["email"] == "pfeiff123456@imag.mail.com"
    assert recv_dict["data"]["token"] is not None

    token = recv_dict["data"]["token"]
    # request the user data
    sock = get_sock()
    data = {
        "request": "GET",
        "type": "user",
        "data": {
            "auth_type": "token",
            "token": token
        }
    }
    send_text(sock, json.dumps(data))

    # get back the user data
    recv_message = receive_text(sock)
    recv_dict: dict = json.loads(recv_message)
    assert not recv_dict["error"]
    assert recv_dict["data"]["email"] == "pfeiff123456@imag.mail.com"
    assert recv_dict["data"]["token"] == token

def test_get_user_invalid():
    """Test invalid get requests for users"""

    data = [({
            "request": "GET",
            "type": "user",
            "data": {
                "email": "pfeiff123456@imag.mail.com",
                "pw_hash": "abcde"
            }
        }, "Missing key 'auth_type' in request "),
        ({
            "request": "GET",
            "type": "user",
            "data": {
                "auth_type": "password",
                "pw_hash": "abcde"
            }
        }, "Missing key 'email' in request "),
        ({
            "request": "GET",
            "type": "user",
            "data": {
                "auth_type": "password",
                "email": "pfeiff123456@imag.mail.com"
            }
        }, "Missing key 'pw_hash' in request "),
        ({
            "request": "GET",
            "type": "user",
            "data": {
                "auth_type": "token"
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
        recv_dict: dict = json.loads(recv_message)

        assert recv_dict["error"]
        assert recv_dict["data"] == f"{error}{json.dumps(request)}".replace('"', "'")
