import json

def validate_request(message: str) -> str | None:
    try:
        message: dict = json.loads(message)
        assert type(message) == dict
    except (json.JSONDecodeError, AssertionError):
        return f"Could not decode request {message}"

    if not "request" in message.keys():
        return f"Missing key 'request' in request {message}"
    if message["request"] not in ["GET", "PUT"]:
        return f"Invalid value '{message['request']}' for key 'request' in request {message}"

    if not "type" in message.keys():
        return f"Missing key 'type' in request {message}"
    if message["type"] not in ["token", "book", "user", "salt", "borrow"]:
        return f"Invalid value '{message['type']}' for key 'type' in request {message}"

    if not ((message["type"] == "user" and message["request"] == "GET") or (message["type"] == "token" and message["request"] == "GET")) and not "data" in message.keys():
        return f"Missing key 'data' in request {message}"

    if message["type"] == "salt":
        return _val_salt_dict(message)

    if not (message["type"] == "user" and message["request"] == "PUT"):
        if not "auth" in message.keys():
            return f"Missing key 'auth' in request {message}"

        err_msg = _val_auth_dict(message)
        if err_msg is not None:
            return err_msg

    if message["type"] == "book":
        return _val_book_dict(message)
    elif message["type"] == "borrow":
        return _val_borrow_dict(message)
    elif message["type"] == "user":
        return _val_user_dict(message)
    elif message["type"] == "token":
        return _val_token_dict(message)

def _val_auth_dict(message: dict):
    auth_dict = message["auth"]

    if not "type" in auth_dict.keys():
        return f"Missing key 'type' in request {message}"

    auth_keys = ["type"]
    if auth_dict["type"] == "token":
        auth_keys += ["token"]
    elif auth_dict["type"] == "password":
        auth_keys += ["email", "pw_hash"]
    else:
        return f"Invalid value '{auth_dict['type']}' for key 'type' in request {message}"

    for key in auth_keys:
        if not key in auth_dict.keys():
            return f"Missing key '{key}' in request {message}"
        if auth_dict[key] == "" or auth_dict[key] is None:
            return f"Invalid value '{auth_dict[key]}' for key '{key}' in request {message}"

    if len(auth_dict.keys()) > len(auth_keys):
        return f"Unnecessary key '{auth_dict.keys()[0]}' in request {message}"

    return None

def _val_salt_dict(message: dict):
    salt_dict: dict = message["data"]

    if message["request"] == "GET":
        salt_keys = ["email"]
    elif message["request"] == "PUT":
        return f"Invalid value 'PUT' for key 'request' for 'type'='salt' in request {message}"

    for key in salt_keys:
        if not key in salt_dict.keys():
            return f"Missing key '{key}' in request {message}"

    if len(salt_dict.keys()) > len(salt_keys):
        return f"Unnecessary key '{salt_dict.keys()[0]}' in request {message}"

    return None

def _val_book_dict(message: dict):
    book_dict: dict = message["data"]
    
    if message["request"] == "GET":
        if len(book_dict.keys()) > 1:
            book_keys = ["title", "author"]
        else:
            book_keys = [("book_id", "barcode")]
    elif message["request"] == "PUT":
        book_keys = ["title", "author"]

    for key in book_keys:
        if isinstance(key, str) and not key in book_dict.keys():
            return f"Missing key '{key}' in request {message}"
        elif isinstance(key, tuple) and not any([key2 in book_dict.keys() for key2 in key]):
            return f"Missing key '{key}' in request {message}"

    if len(book_dict.keys()) > len(book_keys):
        return f"Unnecessary key '{book_dict.keys()[0]}' in request {message}"

    return None

def _val_borrow_dict(message: dict):
    borrow_dict: dict = message["data"]
    
    if message["request"] == "GET":
        borrow_keys = [("borrow_id", "user_id")]
    elif message["request"] == "PUT":
        borrow_keys = ["book_id"]

    for key in borrow_keys:
        if isinstance(key, str) and not key in borrow_dict.keys():
            return f"Missing key '{key}' in request {message}"
        elif isinstance(key, tuple) and not any([key2 in borrow_dict.keys() for key2 in key]):
            return f"Missing key '{key}' in request {message}"

    if len(borrow_dict.keys()) > len(borrow_keys):
        return f"Unnecessary key '{borrow_dict.keys()[0]}' in request {message}"

    return None

def _val_user_dict(message: dict):
    if message["request"] == "GET":
        return

    user_dict: dict = message["data"]

    if message["request"] == "PUT":
        user_keys = ["email", "pw_hash", "salt"]

    for key in user_keys:
        if not key in user_dict.keys():
            return f"Missing key '{key}' in request {message}"

    if len(user_dict.keys()) > len(user_keys):
        for key in user_dict.keys():
            if key not in user_keys:
                return f"Unnecessary key '{key}' in request {message}"

    return None

def _val_token_dict(message: dict):
    return None
    token_dict: dict = message["data"]

    if message["request"] == "GET":
        token_keys = []
    elif message["request"] == "PUT":
        token_keys = []

    for key in token_keys:
        if not key in token_dict.keys():
            return f"Missing key '{key}' in request {message}"

    if len(token_dict.keys()) > len(token_keys):
        for key in token_dict.keys():
            if key not in token_keys:
                return f"Unnecessary key '{key}' in request {message}"

    return None
