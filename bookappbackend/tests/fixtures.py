"""Fixtures for pytest"""

from socket import create_connection, gethostbyname, socket
import pytest

email = "pytest@mail.com"
password = "Kennwort1"
salt = b""
token = ""

@pytest.fixture
def sock() -> socket:
    """Provide a connected socket"""

    address = gethostbyname("ableytner.ddns.net")
    server_address = (address, 20002)
    sock_conn = create_connection(server_address, timeout=1)
    return sock_conn

@pytest.fixture
def pytestuser() -> dict[str:str|bytes]:
    """Provide the email/password/salt/token for the pytest user"""

    data = {
        "email": email,
        "password": password
    }
    if salt != b"":
        data["salt"] = salt
    if token != "":
        data["token"] = token

    return data
