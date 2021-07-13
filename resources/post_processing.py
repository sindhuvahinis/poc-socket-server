from typing import List

import numpy as np

from protocol.output import Output
from util.serializing import djl_encode


class Preprocessor(object):

    def initialize(self):
        pass

    def postprocess(self, np_list:  List[np.ndarray]) -> Output:
        output = Output()
        int_data = np.arange(9).reshape(3, 3)
        float_data = np.arange(9.0).reshape(3, 3)
        np_list_op = [int_data, float_data]
        byte_arr = djl_encode(np_list_op)
        output.set_content(byte_arr)
        return output