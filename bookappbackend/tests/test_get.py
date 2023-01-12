"""Test the handling of GET requests"""

import json

import bcrypt

from bookappbackend.tests.helpers import get_sock, send_text, receive_text, assert_response

def test_get_book():
    """Test the GET request by creating a book and then requesting it"""

    # request the book creation
    sock = get_sock()

    data = {
        "request": "PUT",
        "type": "book",
        "auth": {
            "type": "token",
            "token": "pytest_token"
        },
        "data": {
            "title": "Schachnovelle",
            "author": "Stefan Zweig"
        }
    }
    send_text(sock, json.dumps(data))

    # get back the book_id
    recv_message = receive_text(sock)
    recv_dict = assert_response(recv_message, [("book_id", int, None)])

    # request the book data
    sock = get_sock()
    data = {
        "request": "GET",
        "type": "book",
        "auth": {
            "type": "token",
            "token": "pytest_token"
        },
        "data": {
            "book_id": recv_dict["data"]["book_id"]
        }
    }
    send_text(sock, json.dumps(data))

    # get back the book data
    recv_message = receive_text(sock)
    assert_response(recv_message, [("author", str, "Stefan Zweig"), ("title", str, "Schachnovelle")])

def test_get_book_invalid():
    """Test invalid get requests for books"""

    data = [({
            "request": "GET",
            "type": "book",
            "auth": {
                "type": "token",
                "token": "pytest_token"
            },
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
        try:
            recv_dict = json.loads(recv_message)
        except json.JSONDecodeError:
            raise Exception(f"{recv_message}")

        assert recv_dict["error"], f"{recv_dict['data']}"
        assert recv_dict["data"] == f"{error}{json.dumps(request)}".replace('"', "'")
