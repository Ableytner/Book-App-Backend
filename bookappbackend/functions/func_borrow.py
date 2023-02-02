"""Functions for everything to do with borrows"""

from bookappbackend.database.db_manager import DBManager

# Disable "catching to general esception", because everything sould be catched
# pylint: disable=W0703

def handle(db_manager: DBManager, request: dict) -> dict | str:
    """The main method, handle the given request"""

    if request["request"] == "GET":
        return get(db_manager, request)
    if request["request"] == "PUT":
        return create(db_manager, request)
    return None

def create(db_manager: DBManager, request: dict):
    """Create the given borrow"""

    try:
        user_id = db_manager.get_user_id_by_token(request["auth"]["token"])
        if user_id is None:
            return f"User with token {request['auth']['token']} not found in request {request}"

        borrow_data = {
            "book_id": request["data"]["book_id"],
            "user_id": user_id
        }

        borrow_dict = db_manager.add_borrow(borrow_data)
        assert isinstance(borrow_dict["borrow_id"], int)
    except Exception:
        return f"Borrow with args {borrow_data if 'borrow_data' in locals() else request['data']} could not be created"
    return borrow_dict

def get(db_manager: DBManager, request: dict) -> dict | list | str:
    """Return a saved borrow"""

    if "borrow_id" in request["data"].keys():
        borrow_dict = db_manager.get_borrow(request["data"]["borrow_id"])
        if borrow_dict is None:
            return f"Borrow with borrow_id {request['data']['borrow_id']} not found"
        return borrow_dict
    elif "user_id" in request["data"].keys():
        user_dict = db_manager.get_user(request["data"]["user_id"])
        if user_dict is None:
            return f"User with user_id {request['data']['user_id']} not found"

        borrow_dict = user_dict["borrows"]
        return borrow_dict
