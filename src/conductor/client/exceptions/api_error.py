from enum import Enum


class APIErrorCode(str, Enum):
    NOT_FOUND = ("NOT_FOUND",)
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    BAD_REQUEST = "BAD_REQUEST"
    REQUEST_TIMEOUT = "REQUEST_TIMEOUT"
    UNKNOWN = "UNKNOWN"


class APIError(BaseException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

        super().__init__(message)

    def __str__(self):
        return "APIError: code={} message={}".format(self.code, self.message)
