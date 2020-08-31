from Enums import HTTP_Types

class HTTPRequest:
    method = ""
    url = ""
    headers = {}
    parameters = {}

    def set_method(self, method):
        self.method = method

    def set_url(self, url):
        self.url = url

    def append_header(self, name, value):
        self.headers[name] = value

    def append_parameter(self, name, value):
        self.parameters[name] = value

    def get_method(self):
        return self.method

    def get_url(self):
        return self.url

    def get_headers(self):
        return self.headers

    def get_parameters(self):
        return self.parameters
