# BookAppBackend


## Overview

This project is the backend for the [BookABook](https://github.com/htlweiz/itp2-projekt-ul-mitabi) android app. It is written in Python using the socketserver module.

The **socketserver** runs on port 20002. Connections can be made using a TCP socket in any programming language. The easiest way in python is to use the **socket.create_connection()** method.

@author: Emanuel Ableitner

## API reference

All of the request data is sent as a single string, which is a json dump of an dictionary. If the string can not be interpreted as a dictionary, the server returns an error. 

All of the following documentation can be interpretet as **"key": "value" (explanation)**. Intendations signal a nested dictionary.

### GET

#### Request token

Client:

- "request": "GET" (Defines the type of request)
- "type": "token" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "password" (the type of authentification)
    - "email": "maxmustermann@mail.com" (The user email)
    - "pw_hash": ""

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "":

#### Request book

Client:

- "request": "GET" (Defines the type of request)
- "type": "book" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (the type of authentification)
    - "token": "arandomtoken" (the token that was received before)
- "data": (A dictionary containing the request data)
    - "book_id": 15 (the book_id of the requested book)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "book_id": 15 (the book_id of the requested book)
    - "title": "Die Schachnovelle" (The book title)
    - "author": "Stefan Zweig" (The book author)
    - "borrow": (A dictionary containing the active borrow of the requested book, or None of the book is not currently borrowed)
        - "borrow_id": 36 (the borrow_id of the borrowed book)
        - "book_id": 15 (the book_id of the book that is borrowed)
        - "user_id": 624 (the user_id of the user who borrowed the book)

#### Request a book via the title

Client:

- "request": "GET" (Defines the type of request)
- "type": "book" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (the type of authentification)
    - "token": "arandomtoken" (the token that was received before)
- "data": (A dictionary containing the request data)
    - "title": "Die Schachnovelle" (the title of the requested book)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "book_id": 15 (the book_id of the requested book)
    - "title": "Die Schachnovelle" (The book title)
    - "author": "Stefan Zweig" (The book author)
    - "borrow": (A dictionary containing the active borrow of the requested book, or None of the book is not currently borrowed)
        - "borrow_id": 36 (the borrow_id of the borrowed book)
        - "book_id": 15 (the book_id of the book that is borrowed)
        - "user_id": 624 (the user_id of the user who borrowed the book)

#### Request all books from an author

Client:

- "request": "GET" (Defines the type of request)
- "type": "book" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (the type of authentification)
    - "token": "arandomtoken" (the token that was received before)
- "data": (A dictionary containing the request data)
    - "author": "Stefan Zweig" (the title of the requested book)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - 0: (A dictionary containing the first book by the specified author)
        - "book_id": 15 (the book_id of the requested book)
        - "title": "Die Schachnovelle" (The book title)
        - "author": "Stefan Zweig" (The book author)
        - "borrow": (A dictionary containing the active borrow of the requested book, or None of the book is not currently borrowed)
            - "borrow_id": 36 (the borrow_id of the borrowed book)
            - "book_id": 15 (the book_id of the book that is borrowed)
            - "user_id": 624 (the user_id of the user who borrowed the book)
    - 1: (A dictionary containing the second book by the specified author)
        - "book_id": 19 (the book_id of the requested book)
        - "title": "Brief einer unbekannten" (The book title)
        - "author": "Stefan Zweig" (The book author)
        - "borrow": None (A dictionary containing the active borrow of the requested book, or None of the book is not currently borrowed)
    - 2: (A dictionary containing the third book by the specified author)
        - "book_id": 24 (the book_id of the requested book)
        - "title": "Die Welt von Gestern" (The book title)
        - "author": "Stefan Zweig" (The book author)
        - "borrow": (A dictionary containing the active borrow of the requested book, or None of the book is not currently borrowed)
            - "borrow_id": 60 (the borrow_id of the borrowed book)
            - "book_id": 24 (the book_id of the book that is borrowed)
            - "user_id": 315 (the user_id of the user who borrowed the book)

#### Request borrow

Client:

- "request": "GET" (Defines the type of request)
- "type": "borrow" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (the type of authentification)
    - "token": "arandomtoken" (the token that was received before)
- "data": (A dictionary containing the request data)
    - "borrow_id": 36 (the borrow_id of the borrow to be requested)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "borrow_id": 36 (the borrow_id of the borrowed book)
    - "book_id": 15 (the book_id of the book that is borrowed)
    - "user_id": 624 (the user_id of the user who borrowed the book)

#### Request all borrows from an user

Client:

- "request": "GET" (Defines the type of request)
- "type": "borrow" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (the type of authentification)
    - "token": "arandomtoken" (the token that was received before)
- "data": (A dictionary containing the request data)
    - "user_id": 315 (the user_id of the borrows to be requested)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - 0: (A dictionary containing the first borrow by the specified user)
        - "borrow_id": 60 (the borrow_id of the borrowed book)
        - "book_id": 23 (the book_id of the book that is borrowed)
        - "user_id": 315 (the user_id of the user who borrowed the book)

### PUT

#### Borrow a book

Client:

- "request": "PUT" (Defines the type of request)
- "type": "book" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (the type of authentification)
    - "token": "arandomtoken" (the token that was received before)
- "data": (A dictionary containing the request data)
    - "book_id": 15 (the book_id of the book to be borrowed)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "borrow_id": 36 (the borrow_id of the borrowed book)
    - "book_id": 15 (the book_id of the book that is borrowed)
    - "user_id": 624 (the user_id of the user who borrowed the book)
