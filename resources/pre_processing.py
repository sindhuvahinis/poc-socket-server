import numpy as np
from typing import List

from util.deserializing import djl_decode


class Preprocessor(object):

    def initialize(self):
        pass

    def preprocess(self, input) -> List[np.ndarray]:
        content = input.get_content()
        if "data" in content:
            data = content["data"]
        elif "body" in content:
            data = content["body"]
        else:
            data = list(content.values())[0]
        nd_list = djl_decode(data)
        return nd_list
