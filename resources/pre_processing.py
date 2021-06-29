import numpy as np


class Preprocessor(object):

    def initialize(self):
        pass

    def preprocess(self):
        int_data = np.arange(9).reshape(3, 3)
        float_data = np.arange(9.0).reshape(3, 3)
        return [int_data, float_data]
