"""
Reference : https://github.com/lanking520/djlsdk
"""
import struct
import numpy as np
from typing import List, Tuple

MAGIC_NUMBER = "NDAR"
VERSION = 2


def _get_byte_as_int(encoded: bytearray, idx: int) -> Tuple[int, int]:
    return encoded[idx], idx + 1


def _get_bytes(encoded: bytearray, idx: int, length: int) -> Tuple[bytes, int]:
    return encoded[idx:idx + length], idx + length


def _get_int(encoded: bytearray, idx: int) -> Tuple[int, int]:
    int_size = 4
    return struct.unpack(">i", encoded[idx:idx + int_size])[0], idx + int_size


def _set_int(value: int) -> bytes:
    return struct.pack(">i", value)


def _get_long(encoded: bytearray, idx: int) -> Tuple[int, int]:
    long_size = 8
    return struct.unpack(">q", encoded[idx:idx + long_size])[0], idx + long_size


def _set_long(value: int) -> bytes:
    return struct.pack(">q", value)


def _get_str(encoded: bytearray, idx: int) -> Tuple[str, int]:
    length = struct.unpack(">h", encoded[idx:idx + 2])[0]
    idx += 2
    return encoded[idx:idx + length].decode("utf8"), idx + length


def _set_str(value: str) -> bytes:
    return struct.pack(">h", len(value)) + bytes(value, "utf8")


def _get_char(encoded: bytearray, idx: int, length: int) -> Tuple[str, int]:
    return encoded[idx:idx + length].decode("utf8"), idx + length


def _set_char(value: str) -> bytes:
    return struct.pack('>H', ord(value))
    # return bytes(value, "utf8")


def shape_encode(shape: Tuple[int], arr: bytearray):
    arr.extend(_set_int(len(shape)))
    layout = ""
    for ele in shape:
        arr.extend(_set_long(ele))
        layout += "?"
    arr.extend(_set_int(len(layout)))
    for ele in layout:
        arr.extend(_set_char(ele))


def shape_decode(encoded: bytearray, idx: int) -> Tuple[Tuple, int]:
    length, idx = _get_int(encoded, idx)
    shape = []
    for _ in range(length):
        dim, idx = _get_int(encoded, idx)
        shape.append(dim)
    _, idx = _get_char(encoded, idx, length)
    return tuple(shape), idx


def djl_encode(ndlist: List[np.ndarray]) -> bytearray:
    arr = bytearray()
    arr.extend(_set_int(len(ndlist)))
    for nd in ndlist:
        arr.extend(_set_str(MAGIC_NUMBER))
        arr.extend(_set_int(VERSION))
        arr.append(0)  # no name
        arr.extend(_set_str("default"))
        arr.extend(_set_str(str(nd.dtype).upper()))
        shape_encode(nd.shape, arr)
        nd_bytes = nd.newbyteorder('>').tobytes("C")
        arr.extend(_set_int(len(nd_bytes)))
        arr.extend(nd_bytes)  # make it big endian
    return arr


def djl_decode(encoded: bytearray) -> List[np.ndarray]:
    idx = 0
    num_ele, idx = _get_int(encoded, idx)
    result = []
    for _ in range(num_ele):
        magic, idx = _get_str(encoded, idx)
        if magic != "NDAR":
            raise AssertionError("magic number is not NDAR, actual " + magic)
        version, idx = _get_int(encoded, idx)
        if version != 2:
            raise AssertionError("require version 2, actual " + str(version))
        flag, idx = _get_byte_as_int(encoded, idx)
        if flag == 1:
            _, idx = _get_str(encoded, idx)
        _, idx = _get_str(encoded, idx)  # ignore sparse format
        datatype, idx = _get_str(encoded, idx)
        shape, idx = shape_decode(encoded, idx)
        data_length, idx = _get_int(encoded, idx)
        data, idx = _get_bytes(encoded, idx, data_length)
        result.append(np.ndarray(shape, np.dtype([('big', datatype.lower())]), data))
    return result
