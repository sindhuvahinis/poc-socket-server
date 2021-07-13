class Request(object):
    def __init__(self):
        self.process_type_code = None
        self.python_file = None
        self.function_name = None
        self.content = None

    def set_process_type_code(self, process_type_code):
        self.process_type_code = process_type_code

    def get_process_type_code(self):
        return self.process_type_code

    def set_python_file(self, python_file):
        self.python_file = python_file

    def get_python_file(self):
        return self.python_file

    def set_function_name(self, function_name):
        self.function_name = function_name

    def get_function_name(self):
        return self.function_name

    def set_content(self, content):
        self.content = content

    def get_content(self):
        return self.content
