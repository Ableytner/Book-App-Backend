"""Functions for everything to do with user tokens"""

from bookappbackend.database.db_manager import DBManager

def handle(db_manager: DBManager, request: dict) -> dict | str:
    """The main method, handle the given request"""

    if request["request"] == "GET":
        return create(db_manager, request)
    return None

def create(db_manager: DBManager, request: dict):
    """Create the given book"""

    user_id = db_manager.get_user_id_by_email(request["auth"]["email"])
    if user_id is None:
        return f"User with email {request['auth']['token']} not found in request {request}"

    db_manager.add_token(user_id)
    user_token = db_manager.get_user_token(user_id)
    return {"token": user_token}
