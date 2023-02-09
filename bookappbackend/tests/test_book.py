"""Test book related requests"""

import json
import pytest

from bookappbackend.tests.helpers import get_sock, send_text, receive_text, assert_response

@pytest.mark.order(5)
def test_put_book(sock, pytestuser):
    """Test adding a book using a PUT request"""

    data = {
        "request": "PUT",
        "type": "book",
        "auth": {
            "type": "token",
            "token": pytestuser["token"]
        },
        "data": {
            "title": "Schachnovelle",
            "author": "Stefan Zweig"
        }
    }
    send_text(sock, json.dumps(data))

    recv_message = receive_text(sock)
    try:
        recv_dict = json.loads(recv_message)
    except json.JSONDecodeError:
        raise Exception(f"{recv_message}")
    assert not recv_dict["error"], f"{recv_dict['data']}"

@pytest.mark.order(5)
def test_put_book_invalid(pytestuser):
    """Test invalid put requests for books"""

    data = [({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": "token",
                "token": pytestuser["token"]
            },
            "data": {
                "title": "Schachnovelle",
            }
        }, "Missing key 'author' in request "),
        ({
            "request": "PUT",
            "type": "book",
            "auth": {
                "type": "token",
                "token": pytestuser["token"]
            },
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
        try:
            recv_dict = json.loads(recv_message)
        except json.JSONDecodeError:
            raise Exception(f"{recv_message}")

        assert recv_dict["error"], f"{recv_dict['data']}"
        assert recv_dict["data"] == f"{error}{json.dumps(request)}".replace('"', "'")

@pytest.mark.order(6)
def test_get_book(pytestuser):
    """Test the GET request by requesting a book"""

    book_id = 1

    # request the book data
    sock = get_sock()
    data = {
        "request": "GET",
        "type": "book",
        "auth": {
            "type": "token",
            "token": pytestuser["token"]
        },
        "data": {
            "book_id": book_id
        }
    }
    send_text(sock, json.dumps(data))

    # get back the book data
    recv_message = receive_text(sock)
    assert_response(recv_message, [("author", str, "Stefan Zweig"), ("title", str, "Schachnovelle")])

@pytest.mark.order(6)
def test_get_book_invalid(pytestuser):
    """Test invalid get requests for books"""

    data = [({
            "request": "GET",
            "type": "book",
            "auth": {
                "type": "token",
                "token": pytestuser["token"]
            },
            "data": {
            }
        }, "Missing key '('book_id', 'barcode', 'title')' in request ")
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
