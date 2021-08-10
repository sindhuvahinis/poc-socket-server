"""
Proof of concept for interprocess communication between java and python
through socket connection
"""
import logging
import os
import socket
import sys

import numpy as np

from process_exec_handler import run_processor
from protocol.request_handler import retrieve_request
from util.arg_parser import ArgParser


class SocketServer(object):
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_name = host
        self.port = int(port)

        # sample data to send
        self.int_data = np.arange(9).reshape(3, 3)
        self.float_data = np.arange(9.0).reshape(3, 3)

    def run_server(self):
        self.sock.bind((self.sock_name, self.port))
        self.sock.listen(128)
        logging.info("[PID] %d", os.getpid())
        logging.info("Python server started.")
        cl_sock, _ = self.sock.accept()
        print("DJL Client is connected")

        while True:
            request = retrieve_request(cl_sock)
            print("Received request from DJL Client")
            response = run_processor(request)
            is_sent = cl_sock.sendall(response)
            if not is_sent:
                print("Response is sent to DJL Client")


if __name__ == "__main__":
    try:
        logging.basicConfig(stream=sys.stdout, format="%(message)s", level=logging.INFO)
        args = ArgParser.python_server_args().parse_args()
        host = args.host
        port = args.port
        server = SocketServer(host, port)
        server.run_server()
    except socket.timeout:
        logging.error("Python server did not receive connection")
    except Exception:
        logging.error("Python server died", exc_info=True)
    exit(1)