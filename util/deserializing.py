import struct
from typing import Tuple, List

import numpy as np

from protocol.input import Input


def get_byte_as_int(encoded: bytearray, idx: int) -> Tuple[int, int]:
    return encoded[idx], idx + 1


def get_bytes(encoded: bytearray, idx: int, length: int) -> Tuple[bytes, int]:
    return encoded[idx:idx + length], idx + length


def get_int(encoded: bytearray, idx: int) -> Tuple[int, int]:
    int_size = 4
    return struct.unpack(">i", encoded[idx:idx + int_size])[0], idx + int_size


def get_str(encoded: bytearray, idx: int) -> Tuple[str, int]:
    length = struct.unpack(">h", encoded[idx:idx + 2])[0]
    idx += 2
    return encoded[idx:idx + length].decode("utf8"), idx + length


def get_char(encoded: bytearray, idx: int) -> Tuple[str, int]:
    chr_size = 2
    return chr(struct.unpack(">h", encoded[idx:idx + chr_size])[0]), idx + chr_size


def get_long(encoded: bytearray, idx: int) -> Tuple[int, int]:
    long_size = 8
    return struct.unpack(">q", encoded[idx:idx + long_size])[0], idx + long_size


def shape_decode(encoded: bytearray, idx: int) -> Tuple[Tuple, int]:
    length, idx = get_int(encoded, idx)
    shape = []
    for _ in range(length):
        dim, idx = get_long(encoded, idx)
        shape.append(dim)
    layout_len, idx = get_int(encoded, idx)
    for _ in range(layout_len):
        _, idx = get_char(encoded, idx)
    return tuple(shape), idx


def input_decode(arr: bytearray) -> Input:
    idx = 0
    input = Input()
    req_id, idx = get_str(arr, idx)
    input.set_request_id(req_id)
    prop_size, idx = get_int(arr, idx)

    for _ in range(prop_size):
        key, idx = get_str(arr, idx)
        val, idx = get_str(arr, idx)
        input.add_property(key, val)

    content_size, idx = get_int(arr, idx)
    for _ in range(content_size):
        key, idx = get_str(arr, idx)
        val_len, idx = get_int(arr, idx)
        val, idx = get_bytes(arr, idx, val_len)
        input.add_content_pair(key, val)

    return input


def djl_decode(encoded: bytearray) -> List[np.ndarray]:
    idx = 0
    num_ele, idx = get_int(encoded, idx)
    result = []
    for _ in range(num_ele):
        magic, idx = get_str(encoded, idx)
        if magic != "NDAR":
            raise AssertionError("magic number is not NDAR, actual " + magic)
        version, idx = get_int(encoded, idx)
        if version != 2:
            raise AssertionError("require version 2, actual " + str(version))
        flag, idx = get_byte_as_int(encoded, idx)
        if flag == 1:
            _, idx = get_str(encoded, idx)
        _, idx = get_str(encoded, idx)  # ignore sparse format
        datatype, idx = get_str(encoded, idx)
        shape, idx = shape_decode(encoded, idx)
        data_length, idx = get_int(encoded, idx)
        data, idx = get_bytes(encoded, idx, data_length)
        result.append(np.ndarray(shape, np.dtype([('big', datatype.lower())]), data))
    return result
