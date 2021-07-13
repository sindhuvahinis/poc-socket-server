class Output(object):
    def __init__(self):
        self.request_id = None
        self.code = None
        self.message = None
        self.properties = dict()
        self.content = None

    def get_request_id(self):
        return self.request_id

    def set_request_id(self, request_id: str):
        self.request_id = request_id

    def get_code(self) -> int:
        return self.code

    def set_code(self, code: int):
        self.code = code

    def get_message(self) -> str:
        return self.message

    def set_message(self, message):
        self.message = message

    def get_properties(self) -> map:
        return self.properties

    def set_properties(self, properties: map):
        self.properties = properties

    def get_content(self) -> map:
        return self.content

    def set_content(self, content: map) -> map:
        self.content = content


