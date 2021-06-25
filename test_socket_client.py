import socket
import numpy as np

from util.data_conversion import djl_decode

if __name__ == "__main__":
    port = 9000
    ipaddress = '127.0.0.1'
    sock = socket.socket()
    sock.connect((ipaddress, port))
    print('Server is connected...')
    data = []
    data = sock.recv(2048)
    print('Data received from server is : ', djl_decode(data))
