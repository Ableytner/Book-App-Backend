from socketserver import TCPServer

from bookappbackend.socketapi.tcpsockethandler import TCPSocketHandler

def main():
    print("Starting server...")
    TCPServer(("192.168.0.154", 20002), TCPSocketHandler).serve_forever()

if __name__ == "__main__":
    main()
