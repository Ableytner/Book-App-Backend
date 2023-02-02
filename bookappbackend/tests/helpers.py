"""Module containing helpers for code tests"""

import json

from socket import create_connection, gethostbyname, socket

def get_sock():
    """Return a connected socket"""

    address = gethostbyname("ableytner.ddns.net")
    server_address = (address, 20002)
    sock = create_connection(server_address, timeout=1)
    return sock

def assert_response(response: str, required_keys: list[tuple[str,type,str|None]] = [], data_is_list: bool = False) -> dict:
    assert response, "ERROR: Received empty reponse"
    assert type(response) == str, f"ERROR: Response type is not str but {type(response)} in response {response}"

    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        raise Exception(f"{response}")

    assert type(response) == dict, f"ERROR: Converted response is not of type dict in response {response}"
    assert all([key in response.keys() for key in ["error", "data"]]), f"ERROR: Missing key 'error|data' in response {response}"

    assert type(response["error"]) == bool, f"ERROR: Error type is not bool in response {response}"
    if response["error"]:
        assert type(response["data"]) == str, f"ERROR: Error data type is not str in response {response}"
        raise Exception(f"ERROR: Received error in response {response}")

    expected_data_type = dict if not data_is_list else list
    assert type(response["data"]) == expected_data_type, f"ERROR: Data type is not {expected_data_type} in response {response}"
    for key, value_type, expected_value in required_keys:
        if not data_is_list:
            assert key in response["data"].keys(), f"ERROR: Missing key '{key}' in response {response}"
            assert type(response["data"][key]) == value_type, f"ERROR: Invalid value type {type(response['data'][key])} for key '{key}' in response {response}"
            if expected_value is not None:
                assert response["data"][key] == expected_value, f"ERROR: Invalid value {response['data'][key]} for key '{key}' in response {response}"
        else:
            for c, data_dict in enumerate(response["data"]):
                exp_val = expected_value[c] if isinstance(expected_value, (list, tuple)) else expected_value
                assert key in data_dict.keys(), f"ERROR: Missing key '{key}' in response {response}"
                assert type(data_dict[key]) == value_type, f"ERROR: Invalid value type {type(data_dict[key])} for key '{key}' in response {response}"
                if exp_val is not None:
                    assert data_dict[key] == exp_val, f"ERROR: Invalid value {data_dict[key]} for key '{key}' in response {response}"

    return response

def send_text(sock: socket, text: str) -> None:
    """Send the text to the socket"""

    sock.send(_string_to_bytes(text))

def receive_text(sock: socket) -> str:
    """Receive text from the socket"""

    return _bytes_to_string(sock.recv(1024))

def _string_to_bytes(text: str) -> bytes:
    return bytes(text, "utf-8")

def _bytes_to_string(text: bytes) -> str:
    return text.decode("utf-8")
