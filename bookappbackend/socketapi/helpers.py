"""Helper functions for using sockets"""

def send_text(self, text: str) -> None:
    """Send a string to the socket"""

    self.request.sendall(_string_to_bytes(text))

def receive_text(self) -> str:
    """Receive a string from the socket"""

    return _bytes_to_string(self.request.recv(1024))

def _string_to_bytes(input: str) -> bytes:
    return bytes(input, "utf-8")

def _bytes_to_string(bytes: bytes) -> str:
    return bytes.decode("utf-8")
