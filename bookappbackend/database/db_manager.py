"""Module for managing the database"""

# pylint: disable=E0401, R0402

from threading import Lock

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from .model import Base, Book, User, Borrow

# pylint: disable=R0801

class DBManager():
    """Class that manages the database"""

    def __init__(self) -> None:
        db_connection = sqlalchemy.create_engine(f"sqlite:///{DBManager.dbfile_path}",
                                                 connect_args={'check_same_thread': False})
        Base.metadata.create_all(db_connection)

        session_factory = sessionmaker(db_connection, autoflush=False)
        _session = scoped_session(session_factory)
        DBManager.session = _session()

        DBManager.lock = Lock()

    dbfile_path = "bookappbackend/database/database.db"
    lock: Lock = None
    session: scoped_session = None

    def add_book(self, book_dict: dict) -> dict:
        """Add a Book to the database"""

        with DBManager.lock:
            try:
                book = Book(title=book_dict["title"], author=book_dict["author"])
            except Exception:
                return {"book_id": -1}
            DBManager.session.add(book)

        self.commit()

        return {"book_id": book.book_id}

    def add_user(self, user_dict: dict) -> dict:
        """Add a User to the database"""

        with DBManager.lock:
            user = User(email=user_dict["email"], pw_hash=user_dict["pw_hash"], token=None)
            DBManager.session.add(user)

        self.commit()

        return {"user_id": user.user_id}

    def add_borrow(self, borrow_dict: dict) -> dict:
        """Add a Borrow to the database"""

        with DBManager.lock:
            borrow = Borrow(expire_date=borrow_dict["expire_date"])
            book = DBManager.session.query(Book).filter(Book.book_id==borrow_dict["book_id"]).first()
            book.borrow.append(book)
            user = DBManager.session.query(User).filter(User.user_id==borrow_dict["user_id"]).first()
            user.borrow.append(book)
            DBManager.session.add(borrow)

        self.commit()

        return {"borrow_id": borrow.borrow_id}

    def add_token(self, user_id: int) -> None:
        """Add a token to an existing user, overwriting the old one"""

        with DBManager.lock:
            token = self._create_token()
            user = self.session.query(User).filter(User.user_id==user_id).first()
            user.token = token
        
        self.commit()

    def commit(self) -> None:
        """Commits changes to database"""

        with DBManager.lock:
            try:
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                self.session.rollback()

    def delete_user(self, user_id: int) -> None:
        """Delete a user from the database"""

        with DBManager.lock:
            self.session.query(User).filter(User.user_id==user_id).delete()
        self.commit()

    def delete_borrow(self, borrow_id: int) -> None:
        """Delete a borrow from the database"""

        with DBManager.lock:
            self.session.query(Borrow).filter(Borrow.borrow_id==borrow_id).delete()
        self.commit()

    def get_book(self, book_id: int) -> dict | None:
        """Return the book with the given book_id"""

        with DBManager.lock:
            book = self.session.query(Book).filter(Book.book_id==book_id).first()
        return self._book_to_dict(book)

    def get_borrow(self, borrow_id: int) -> dict | None:
        """Return the borrow with the given borrow_id"""

        with DBManager.lock:
            borrow = self.session.query(Borrow).filter(Borrow.borrow_id==borrow_id).first()
        return self._borrow_to_dict(borrow)

    def get_user(self, user_id: int) -> dict | None:
        """Return the user with the given user_id"""

        with DBManager.lock:
            user = self.session.query(User).filter(User.user_id==user_id).first()
        return self._user_to_dict(user)

    def get_user_id_by_email(self, email: str) -> int:
        """Return the user_id from the given email"""

        with DBManager.lock:
            user = self.session.query(User).filter(User.email==email).first()
        return user.user_id if user is not None else None

    def get_user_id_by_token(self, token: str) -> int:
        """Return the user_id from the given token"""

        with DBManager.lock:
            user = self.session.query(User).filter(User.token==token).first()
        return user.user_id if user is not None else None

    def update_user(self, user_dict: dict) -> None:
        with DBManager.lock:
            user: User = self.session.query(User).filter(User.user_id==user_dict["user_id"]).first()
            user.name = user_dict["name"]
            user.email = user_dict["email"]
            user.pw_hash = user_dict["pw_hash"]
        self.commit()

    def _user_to_dict(self, user: User):
        if user is None:
            return None

        user_dict = {
            "user_id": user.user_id,
            "email": user.email,
            "token": user.token
        }

        if user.borrow is None:
            user_dict["borrows"] = []
        else:
            borrow_list = []
            for borrow in user.borrow:
                borrow_list.append(self._borrow_to_dict(borrow))
            user_dict["borrows"] = borrow_list

        return user_dict

    def _book_to_dict(self, book: Book):
        if book is None:
            return None

        book_dict = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author
        }

        if book.borrow is None:
            book_dict["borrows"] = []
        else:
            borrow_list = []
            for borrow in book.borrow:
                borrow_list.append(self._borrow_to_dict(borrow))
            book_dict["borrows"] = borrow_list

        return book_dict

    def _borrow_to_dict(self, borrow: Borrow):
        if borrow is None:
            return None
        return {"borrow_id": borrow.borrow_id, "book_id": borrow.book_id, "user_id": borrow.user_id}

    def _create_token(self):
        return "asecuretoken"
