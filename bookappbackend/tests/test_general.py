"""Test general requests"""

import json

from bookappbackend.tests.helpers import send_text, receive_text, get_sock

def test_invalid():
    """Test invalid requests"""
    data = [({
            "type": "",
            "data": {}
        }, "Missing key 'request' in request ")
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
    error_msg = f"Could not decode request "

    for data_corr in data_corrs:
        sock = get_sock()
        send_text(sock, data_corr)

        recv_message = receive_text(sock)
        recv_dict: dict = json.loads(recv_message)
        assert recv_dict["error"]
        assert recv_dict["data"] == f"{error_msg}{data_corr}"