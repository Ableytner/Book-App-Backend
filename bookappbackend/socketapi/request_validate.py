import json

def validate_request(message: str) -> str:
    try:
        message: dict = json.loads(message)
        assert type(message) == dict
    except (json.JSONDecodeError, AssertionError):
        return True, f"Could not decode request {message}"

    if not "request" in message.keys():
        return True, f"Missing key 'request' in request {message}"
    if message["request"] not in ["GET", "PUT"]:
        return True, f"Invalid value '{message['request']}' for key 'request' in request {message}"

    if not "type" in message.keys():
        return True, f"Missing key 'type' in request {message}"
    if not "data" in message.keys():
        return True, f"Missing key 'data' in request {message}"

    if message["type"] == "book":
        return _val_book_dict(message)
    elif message["type"] == "user":
        return _val_user_dict(message)

def _val_book_dict(message: str):
    book_dict: dict = message["data"]
    
    if message["request"] == "GET":
        book_keys = ["book_id"]
    elif message["request"] == "PUT":
        book_keys = ["title", "author"]

    for key in book_keys:
        if not key in book_dict.keys():
            return True, f"Missing key '{key}' in request {message}"

    return False, ""

def _val_user_dict(message: str):
    user_dict: dict = message["data"]
    
    if message["request"] == "GET":
        if not "auth_type" in user_dict.keys():
            return True, f"Missing key 'auth_type' in request {message}"

        if user_dict["auth_type"] == "token":
            user_keys = ["token"]
        elif user_dict["auth_type"] == "password":
            user_keys = ["email", "pw_hash"]
        else:
            return True, f"Invalid value '{user_dict['auth_type']}' for key 'auth_type' in request {message}"
    elif message["request"] == "PUT":
        user_keys = ["email", "pw_hash"]

    for key in user_keys:
        if not key in user_dict.keys():
            return True, f"Missing key '{key}' in request {message}"

    return False, ""
