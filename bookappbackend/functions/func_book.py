from bookappbackend.database.db_manager import DBManager

def handle(db_manager: DBManager, request: dict) -> dict | str:
    if request["request"] == "GET":
        return get(db_manager, request)
    if request["request"] == "PUT":
        return create(db_manager, request)

def create(db_manager: DBManager, request: dict):
    try:
        book_dict = db_manager.add_book(request["data"])
        assert type(book_dict["book_id"]) == int
    except Exception:
        return f"Book with args {request['data']} could not be created"
    return book_dict

def get(db_manager: DBManager, request: dict):
    book_dict = db_manager.get_book(request["data"]["book_id"])
    if book_dict is None:
        return f"Book with book_id {request['data']['book_id']} not found"
    return book_dict
