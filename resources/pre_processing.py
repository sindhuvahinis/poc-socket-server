import numpy as np
from typing import List

from util.deserializing import djl_decode


class Preprocessor(object):

    def initialize(self):
        pass

    def preprocess(self, input) -> List[np.ndarray]:
        content = input.get_content()
        pair_keys = content.get_keys()
        if "data" in pair_keys:
            data = content.get(key="data")
        elif "body" in pair_keys:
            data = content.get(key="body")
        else:
            data = list(content.get_values())[0]
        nd_list = djl_decode(data)
        return data
