"""Test borrow related requests"""

import json
import pytest

import bookappbackend.tests.fixtures as fixtures
from bookappbackend.tests.helpers import send_text, receive_text, get_sock, assert_response

@pytest.mark.order(10)
def test_put_borrow(sock, pytestuser):
    data = {
        "request": "PUT",
        "type": "borrow",
        "auth": {
            "type": "token",
            "token": pytestuser["token"]
        },
        "data": {
            "book_id": "1",
        }
    }
    send_text(sock, json.dumps(data))

    recv_message = receive_text(sock)
    try:
        recv_dict = json.loads(recv_message)
    except json.JSONDecodeError:
        raise Exception(f"{recv_message}")
    assert not recv_dict["error"], f"{recv_dict['data']}"

@pytest.mark.order(11)
def test_get_borrow(pytestuser):
    """Test the GET request by requesting a borrow"""

    borrow_id = 1

    sock = get_sock()
    data = {
        "request": "GET",
        "type": "borrow",
        "auth": {
            "type": "token",
            "token": pytestuser["token"]
        },
        "data": {
            "borrow_id": borrow_id
        }
    }
    send_text(sock, json.dumps(data))

    recv_message = receive_text(sock)
    assert_response(recv_message, [("borrow_id", int, 1), ("user_id", int, 1), ("book_id", int, 1)])

@pytest.mark.order(12)
def test_get_all_borrows(pytestuser):
    """Test the GET request by requesting all borrows from a user"""

    user_id = 1

    sock = get_sock()
    data = {
        "request": "GET",
        "type": "borrow",
        "auth": {
            "type": "token",
            "token": pytestuser["token"]
        },
        "data": {
            "user_id": user_id
        }
    }
    send_text(sock, json.dumps(data))

    recv_message = receive_text(sock)
    assert_response(recv_message, [("borrow_id", int, 1), ("user_id", int, 1), ("book_id", int, 1)], data_is_list=True)
