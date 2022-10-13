import json
import socketserver

from bookappbackend.database.db_manager import DBManager
from bookappbackend.socketapi.helpers import send_text, receive_text
from bookappbackend.socketapi.request_validate import validate_request

class TCPSocketHandler(socketserver.BaseRequestHandler):
    db_manager = DBManager()
    
    def handle(self):
        print('Client ' + str(self.client_address[0]) + ' connected!')

        message = receive_text(self)
        error, val_result = validate_request(message)
        if error:
            self._send_result(error, val_result)
            print('Client ' + str(self.client_address[0]) + ' disconnected!')
            return

        message: dict = json.loads(message)

        if message["request"] == "GET":
            print(f"Received data {message}")
            res_error, res_data = self._get(message)
        elif message["request"] == "PUT":
            print(f"Received data {message}")
            res_error, res_data = self._put(message)
        else:
            print(f"ERROR: Received unknown request {message['request']} with data {message}")

        self._send_result(res_error, res_data)
        print('Client ' + str(self.client_address[0]) + ' disconnected!')

    def _get(self, message: dict):
        if message["type"] == "book":
            book_dict = self.db_manager.get_book(message["data"]["book_id"])
            if book_dict is None:
                return True, f"Book with book_id {message['data']['book_id']} not found"
            return False, book_dict
        elif message["type"] == "user":
            user_dict = self.db_manager.get_user(message["data"]["user_id"])
            if user_dict is None:
                return True, f"User with user_id {message['data']['user_id']} not found"
            return False, user_dict

    def _put(self, message: dict):
        if message["type"] == "book":
            book_dict = self.db_manager.add_book(message["data"])
            if book_dict["book_id"] == -1:
                return True, f"Book with args {message['data']} could not be created"
            return False, book_dict
        elif message["type"] == "user":
            user_dict = self.db_manager.add_user(message["data"])
            if user_dict["user_id"] == -1:
                return True, f"User with args {message['data']} could not be created"
            return False, user_dict

    def _send_result(self, res_error: bool, res_data: dict):
        res_dict = {
            "error": res_error,
            "data": res_data
        }
        print(f"Sending data {res_dict}")
        send_text(self, json.dumps(res_dict))
