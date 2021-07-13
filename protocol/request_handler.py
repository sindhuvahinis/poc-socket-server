import logging
import struct

import numpy as np

from protocol.input import Input
from protocol.request import Request

char_size = 2
short_size = 2
int_size = 4
long_size = 8

MAGIC_NUMBER = "NDAR"
VERSION = 2


def _retrieve_buffer(conn, length):
    data = bytearray()

    while length > 0:
        pkt = conn.recv(length)
        if len(pkt) == 0:
            logging.info("Frontend disconnected.")
            raise ValueError("Frontend disconnected")

        data += pkt
        length -= len(pkt)

    return data


def _retrieve_char(conn):
    data = _retrieve_buffer(conn, char_size)
    return chr(struct.unpack(">h", data)[0])


def _retrieve_int(conn):
    data = _retrieve_buffer(conn, int_size)
    return struct.unpack("!i", data)[0]


def _retrieve_str(conn):
    length_buf = _retrieve_buffer(conn, short_size)
    length = struct.unpack(">h", length_buf)[0]
    data = _retrieve_buffer(conn, length)
    return data.decode("utf8")


def _retrieve_long(conn):
    data = _retrieve_buffer(conn, long_size)
    return struct.unpack(">q", data)[0]


def _retrieve_shape(conn):
    length = _retrieve_int(conn)
    shape = []
    for _ in range(length):
        dim = _retrieve_long(conn)
        shape.append(dim)
    layout_len = _retrieve_int(conn)
    for _ in range(layout_len):
        _ = _retrieve_char(conn)
    return tuple(shape)


def retrieve_ndlist(conn):
    num_ele = _retrieve_int(conn)
    result = []
    for _ in range(num_ele):
        magic = _retrieve_str(conn)
        if magic != MAGIC_NUMBER:
            raise AssertionError("magic number is not NDAR, actual " + magic)

        version = _retrieve_int(conn)
        if version != VERSION:
            raise AssertionError("require version 2, actual " + str(version))
        flag = _retrieve_buffer(conn)
        if flag == 1:
            _ = _retrieve_str(conn)
        _ = _retrieve_str(conn)  # ignore sparse format
        datatype = _retrieve_str(conn)
        shape, idx = _retrieve_shape(conn)
        data_length, idx = _retrieve_int(conn)
        data, idx = _retrieve_buffer(conn, data_length)
        result.append(np.ndarray(shape, np.dtype([('big', datatype.lower())]), data))
    return result


def retrieve_processing_file(conn):
    decoded_map = dict()

    process_type_code = _retrieve_int(conn)
    decoded_map["process_type_code"] = process_type_code

    file_path = _retrieve_str(conn)
    decoded_map["python_file_path"] = file_path

    function_name = _retrieve_str(conn)
    decoded_map["function_name"] = function_name

    return decoded_map


def retrieve_request(conn):
    request = Request()

    process_type_code = _retrieve_int(conn)
    request.set_process_type_code(process_type_code)

    python_file = _retrieve_str(conn)
    request.set_python_file(python_file)

    function_name = _retrieve_str(conn)
    request.set_function_name(function_name)

    content_len = _retrieve_int(conn)
    content = _retrieve_buffer(conn, content_len)
    request.set_content(content)

    return request


def retrieve_input_data(conn):
    input = Input()
    req_id = _retrieve_str(conn)
    input.set_request_id(req_id)
    map_size = _retrieve_int(conn)
    for _ in range(map_size):
        key = _retrieve_str(conn)
        val = _retrieve_str(conn)
        input.add_property(key, val)

    content_size = _retrieve_int(conn)
    for _ in range(content_size):
        key = _retrieve_str(conn)
        val_len = _retrieve_int(conn)
        val = _retrieve_buffer(conn, val_len)
        input.add_content_pair(key, val)

    return input
