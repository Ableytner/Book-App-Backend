def send_text(self, text):
    self.request.sendall(_string_to_bytes(text))

def receive_text(self):
    return _bytes_to_string(self.request.recv(1024))

def _string_to_bytes(input):
    return bytes(input, "utf-8")

def _bytes_to_string(bytes):
    return bytes.decode("utf-8")
