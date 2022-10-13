"""Declaring data models"""

import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.orm import relationship

Base = sqlalchemy.ext.declarative.declarative_base()

# pylint: disable=R0903

class Book(Base):
    """Book representation."""

    __tablename__ = "book"
    book_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    borrow = relationship("Borrow", cascade="all,delete", uselist=False, backref="book")

class User(Base):
    """User representation."""

    __tablename__ = "user"
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    pw_hash = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    borrow = relationship("Borrow", cascade="all,delete", uselist=False, backref="user")

class Borrow(Base):
    """Book and User crosstable"""

    __tablename__ = "borrow"
    borrow_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.user_id"))
    book_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("book.book_id"))
    expire_date = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
