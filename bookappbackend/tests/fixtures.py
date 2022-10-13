"""Fixtures for pytest"""

from socket import create_connection, gethostbyname
import pytest

@pytest.fixture
def sock():
    """Provide a connected socket"""

    address = gethostbyname("ableytner.ddns.net")
    server_address = (address, 20002)
    sock_conn = create_connection(server_address, timeout=1)
    return sock_conn
