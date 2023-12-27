# -*- coding: utf-8 -*-

import sys

class SDKException(Exception):
    """enginefaas sdk 异常类"""

    def __init__(self, code=None, message=None, requestId=None):
        self.code = code
        self.message = message
        self.requestId = requestId

    def __str__(self):
        s = "[SDKException] code:%s message:%s requestId:%s" % (
            self.code, self.message, self.requestId)
        if sys.version_info[0] < 3 and isinstance(s, unicode):
            return s.encode("utf8")
        else:
            return s

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def get_request_id(self):
        return self.requestId
