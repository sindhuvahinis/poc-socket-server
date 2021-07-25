"""
Reference : https://github.com/lanking520/djlsdk
"""
import struct
import numpy as np
from typing import List, Tuple

MAGIC_NUMBER = "NDAR"
VERSION = 2


def _set_int(value: int) -> bytes:
    return struct.pack(">i", value)


def _set_long(value: int) -> bytes:
    return struct.pack(">q", value)


def _set_str(value: str) -> bytes:
    return struct.pack(">h", len(value)) + bytes(value, "utf8")


def _set_char(value: str) -> bytes:
    return struct.pack('>h', ord(value))


def shape_encode(shape: Tuple[int], arr: bytearray):
    arr.extend(_set_int(len(shape)))
    layout = ""
    for ele in shape:
        arr.extend(_set_long(ele))
        layout += "?"
    arr.extend(_set_int(len(layout)))
    for ele in layout:
        arr.extend(_set_char(ele))


def djl_encode(ndlist: List[np.ndarray]) -> bytearray:
    arr = bytearray()
    arr.extend(_set_int(len(ndlist)))
    for nd in ndlist:
        arr.extend(_set_str(MAGIC_NUMBER))
        arr.extend(_set_int(VERSION))
        arr.append(0)  # no name
        arr.extend(_set_str("default"))
        arr.extend(_set_str(str(nd.dtype[0]).upper()))
        shape_encode(nd.shape, arr)
        nd_bytes = nd.newbyteorder('>').tobytes("C")
        arr.extend(_set_int(len(nd_bytes)))
        arr.extend(nd_bytes)  # make it big endian
    return arr


def output_encode(output) -> bytearray:
    arr = bytearray()
    arr.extend(_set_str(output.get_request_id()))
    arr.extend(_set_int(output.get_code()))
    arr.extend(_set_str(output.get_message()))

    properties = output.get_properties()
    map_size = len(properties)
    arr.extend(_set_int(map_size))
    if properties:
        for key, val in output.get_properties().items():
            arr.extend(_set_str(key))
            arr.extend(_set_str(val))

    content = output.content
    arr.extend(_set_int(len(content)))
    arr.extend(content)
    return arr


def response_encode(response) -> bytearray:
    arr = bytearray()
    arr.extend(_set_int(response.len))
    arr.extend(response.buffer_arr)
    return arr
