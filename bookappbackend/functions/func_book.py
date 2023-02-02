"""Functions for everything to do with books"""

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
    """Create the given book"""

    try:
        book_dict = db_manager.add_book(request["data"])
        assert isinstance(book_dict["book_id"], int)
    except Exception:
        return f"Book with args {request['data']} could not be created"
    return book_dict

def get(db_manager: DBManager, request: dict):
    """Return a saved book"""

    if "book_id" in request["data"].keys():
        book_dict = db_manager.get_book(request["data"]["book_id"])
        if book_dict is None:
            return f"Book with book_id {request['data']['book_id']} not found"
        return book_dict
    elif "barcode" in request["data"].keys():
        book_dict = db_manager.get_book_by_barcode(request["data"]["barcode"])
        if book_dict is None:
            return f"Book with barcode {request['data']['barcode']} not found"
        return book_dict
