"""
Proof of concept for interprocess communication between java and python
through socket connection
"""
import socket
import numpy as np

from util.data_conversion import djl_encode


class SocketServer(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

            cl_num = 0
            while True:
                cl_num += 1
                cl_sock, _ = self.sock.accept()
                print(f"Client {cl_num} is connected")
                # cl_sock.send('Python server is connected'.encode())
                data = djl_encode([self.int_data, self.float_data])
                is_sent = cl_sock.sendall(data)

                if not is_sent:
                    print('Data is sent')

                cl_sock.close()
                print(f"Client {cl_num} connection is closed")
        finally:
            self.sock.close()


if __name__ == "__main__":
    server = SocketServer()
    server.run_server()
