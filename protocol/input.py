from util.pair_list import PairList


class Input(object):
    def __init__(self):
        self.request_id = None
        self.properties = dict()
        self.content = PairList() #ndlist/tensor

    def get_request_id(self) -> str:
        return self.request_id

    def get_properties(self) -> map:
        return self.properties

    def get_content(self) -> PairList:
        return self.content

    def get_properties_value(self, key: str) -> str:
        return self.properties[key]

    def set_request_id(self, request_id: str):
        self.request_id = request_id

    def set_properties(self, properties: map):
        self.properties = properties

    def set_content(self, content: PairList):
        self.content = content

    def add_property(self, key: str, val: str):
        self.properties[key] = val

    def get_as_numpy(self, key=None):
        # return list of values as numpy if not provided key
        pass
    



