class Response(object):
    def __init__(self):
        self.len = None
        self.buffer_arr = None

    def get_len(self):
        return self.len

    def set_len(self, len):
        self.len = len

    def get_buffer_arr(self):
        return self.buffer_arr

    def set_buffer_arr(self, buffer_arr):
        self.buffer_arr = buffer_arr
