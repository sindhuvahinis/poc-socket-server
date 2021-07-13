class Input(object):
    def __init__(self):
        self.request_id = None
        self.properties = dict()
        self.content = dict()

    def get_request_id(self) -> str:
        return self.request_id

    def get_properties(self) -> map:
        return self.properties

    def get_content(self) -> map:
        return self.content

    def get_properties_value(self, key: str) -> str:
        return self.properties[key]

    def set_request_id(self, request_id: str):
        self.request_id = request_id

    def set_properties(self, properties: map):
        self.properties = properties

    def set_content(self, content: map):
        self.content = content

    def add_property(self, key: str, val: str):
        self.properties[key] = val

    def add_content_pair(self, key: str, val: str):
        self.content[key] = val




