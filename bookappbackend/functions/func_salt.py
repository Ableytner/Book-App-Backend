from bookappbackend.database.db_manager import DBManager

def handle(db_manager: DBManager, request: dict) -> dict | str:
    if request["request"] == "GET":
        return get(db_manager, request)

def get(db_manager: DBManager, request: dict) -> dict | str:
    user_id = db_manager.get_user_id_by_email(request["data"]["email"])
    if user_id is None:
        return f"User with email {request['data']['email']} not found"
    salt = db_manager.get_salt(user_id)
    return {"salt": salt}
