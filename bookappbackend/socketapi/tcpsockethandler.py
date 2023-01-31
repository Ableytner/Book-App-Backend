import json
import socketserver

from bookappbackend.database.db_manager import DBManager
from bookappbackend.socketapi.helpers import send_text, receive_text
from bookappbackend.socketapi.request_validate import validate_request
from bookappbackend.functions import func_salt, func_book, func_borrow, func_user, func_token

class TCPSocketHandler(socketserver.BaseRequestHandler):
    db_manager = DBManager()
    
    def handle(self):
        print('Client ' + str(self.client_address[0]) + ' connected!')

        message = receive_text(self).replace("\n", "")
        print(f"Received data {message}")
        val_result = validate_request(message)
        # if validate_request returned an error, sent the error and exit
        if val_result is not None:
            self._send_result(val_result)
            print('Client ' + str(self.client_address[0]) + ' disconnected!')
            return

        message: dict = json.loads(message)

        if message["type"] == "salt":
            res_data = func_salt.handle(self.db_manager, message)
            if type(res_data) == str:
                self._send_result(res_data)
                print('Client ' + str(self.client_address[0]) + ' disconnected!')
                return

        if message["type"] == "book":
            res_data = func_book.handle(self.db_manager, message)
        elif message["type"] == "borrow":
            res_data = func_borrow.handle(self.db_manager, message)
        elif message["type"] == "user":
            res_data = func_user.handle(self.db_manager, message)
        elif message["type"] == "token":
            res_data = func_token.handle(self.db_manager, message)

        self._send_result(res_data)
        print('Client ' + str(self.client_address[0]) + ' disconnected!')

    def _get(self, message: dict):
        if message["type"] == "book":
            book_dict = self.db_manager.get_book(message["data"]["book_id"])
            if book_dict is None:
                return True, f"Book with book_id {message['data']['book_id']} not found"
            return False, book_dict
        elif message["type"] == "user":
            if message["data"]["auth_type"] == "password":
                user_id = self.db_manager.get_user_id_by_email(message["data"]["email"])
                self.db_manager.add_token(user_id)
            else:
                user_id = self.db_manager.get_user_id_by_token(message["data"]["token"])
            if user_id is None:
                return True, f"User not found in request {message}"
            return False, self.db_manager.get_user(user_id)

    def _put(self, message: dict):
        if message["type"] == "book":
            book_dict = self.db_manager.add_book(message["data"])
            if book_dict["book_id"] == None:
                return True, f"Book with args {message['data']} could not be created"
            return False, book_dict
        elif message["type"] == "user":
            user_dict = self.db_manager.add_user(message["data"])
            if user_dict["user_id"] == None:
                return True, f"User with args {message['data']} could not be created"
            return False, user_dict

    def _send_result(self, res_data: dict | str):
        res_dict = {
            "error": type(res_data) == str,
            "data": res_data
        }
        print(f"Sending data {res_dict}")
        send_text(self, json.dumps(res_dict))
