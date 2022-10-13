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

def test_get_book_mising_bookid_key(sock):
    """Test a get request missing the 'book_id' key"""

    data = {
        "request": "GET",
        "type": "book",
        "data": {
        }
    }
    send_text(sock, json.dumps(data))

    recv_message = receive_text(sock)
    recv_dict: dict = json.loads(recv_message)
    assert recv_dict["error"]
    assert recv_dict["data"] == f"Missing key 'book_id' in request {data}"
