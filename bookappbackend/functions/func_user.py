from bookappbackend.database.db_manager import DBManager

def handle(db_manager: DBManager, request: dict) -> dict | str:
    if request["request"] == "GET":
        return get(db_manager, request)
    if request["request"] == "PUT":
        return create(db_manager, request)

def create(db_manager: DBManager, request: dict):
    try:
        user_dict = db_manager.add_user(request["data"])
        assert type(user_dict["user_id"]) == int
    except Exception:
        return f"User with args {request['data']} could not be created in request {request}"
    return user_dict

def get(db_manager: DBManager, request: dict):
    user_id = db_manager.get_user_id_by_token(request["auth"]["token"])
    user_dict = db_manager.get_user(user_id)

    if user_id is None or user_dict is None:
        return f"User with token {request['auth']['token']} not found in request {request}"
    return user_dict
