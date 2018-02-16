
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
