"""Module containing helpers for code tests"""

from socket import create_connection, gethostbyname, socket

def get_sock():
    """Return a connected socket"""

    address = gethostbyname("ableytner.ddns.net")
    server_address = (address, 20002)
    sock = create_connection(server_address, timeout=1)
    return sock

def send_text(sock: socket, text: str) -> None:
    """Send the text to the socket"""

    sock.send(_string_to_bytes(text))

def receive_text(sock: socket) -> str:
    """Receive text from the socket"""

    return _bytes_to_string(sock.recv(1024))

def _string_to_bytes(text: str) -> bytes:
    return bytes(text, "utf-8")

def _bytes_to_string(text: bytes) -> str:
    return text.decode("utf-8")
