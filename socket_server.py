"""
Proof of concept for interprocess communication between java and python
through socket connection
"""
import socket
import numpy as np

from process_exec_handler import run_processor
from protocol.request_handler import retrieve_request


class SocketServer(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_name = "127.0.0.1"
        self.port = 9000

        # sample data to send
        self.int_data = np.arange(9).reshape(3, 3)
        self.float_data = np.arange(9.0).reshape(3, 3)

    def run_server(self):
        try:
            self.sock.bind((self.sock_name, self.port))
            self.sock.listen(128)
            print('Server is started...')

            cl_sock, _ = self.sock.accept()
            print(f"Client is connected")

            while True:
                request = retrieve_request(cl_sock)
                response = run_processor(request)
                is_sent = cl_sock.sendall(response)
                if not is_sent:
                    print("Response is all sent")
        except:
            print("Client is disconnected")
        finally:
            self.sock.close()
            print("Server is shutdown")


if __name__ == "__main__":
    server = SocketServer()
    server.run_server()
