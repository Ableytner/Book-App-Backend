def send_text(self, text) -> None:
    self.request.sendall(_string_to_bytes(text))

def receive_text(self) -> str:
    return _bytes_to_string(self.request.recv(1024))

def _string_to_bytes(input) -> bytes:
    return bytes(input, "utf-8")

def _bytes_to_string(bytes) -> str:
    return bytes.decode("utf-8")
