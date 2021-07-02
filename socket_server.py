"""
Proof of concept for interprocess communication between java and python
through socket connection
"""
import socket
import numpy as np

from protocol.recv_data_handler import retrieve_processing_file
from util.data_conversion import djl_encode
from util.packaging_utils import get_class_name


def receive_python_file(cl_sock):
    decoded = retrieve_processing_file(cl_sock)
    print(f"Data received is {decoded}")
    return decoded


def run_processor(decoded):
    processor_type = "pre-process" if decoded["process_type_code"] == 0 else "post-process"
    processor_class = get_class_name(decoded["python_file_path"], decoded["function_name"])
    preprocessor = processor_class()
    data = getattr(preprocessor, decoded["function_name"])()
    print(f'{processor_type} data {data}')
    return data


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

            cl_num = 0
            while True:
                cl_num += 1
                cl_sock, _ = self.sock.accept()
                print(f"Client {cl_num} is connected")

                decoded = receive_python_file(cl_sock)
                data_list = run_processor(decoded)
                byte_data = djl_encode(data_list)
                is_sent = cl_sock.sendall(byte_data)
                if not is_sent:
                    print('Data is sent')

                cl_sock.close()
                print(f"Client {cl_num} connection is closed")
        finally:
            self.sock.close()


if __name__ == "__main__":
    server = SocketServer()
    server.run_server()
