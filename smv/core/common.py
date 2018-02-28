
RESPONSE_OK = object()
RESPONSE_ERROR = object()
RESPONSE_WARN = object()


class Response(object):

    def __init__(self):
        self.content = ""
        self.return_code = RESPONSE_OK

    @staticmethod
    def success(response_content=""):
        r = Response()
        r.content = response_content
        r.return_code = RESPONSE_OK
        return r

    @staticmethod
    def error(response_content=""):
        response = Response()
        response.content = response_content
        response.return_code = RESPONSE_ERROR
        return response

    def is_error(self):
        return self.return_code == RESPONSE_ERROR


class SupportedOutputFormats:
    image = "image"
    text = "text"
    json = "json"

    @staticmethod
    def is_in(value):
        return value in (SupportedOutputFormats.image,SupportedOutputFormats.text,SupportedOutputFormats.json)
