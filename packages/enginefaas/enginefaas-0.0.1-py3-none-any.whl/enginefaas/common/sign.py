# -*- coding: utf-8 -*-

import binascii
import hashlib
import hmac
import sys

from enginefaas.common.exception.sdk_exception import SDKException


class Sign(object):

    @staticmethod
    def sign(secret_key, sign_str, sign_method):
        if sys.version_info[0] > 2:
            sign_str = bytes(sign_str, 'utf-8')
            secret_key = bytes(secret_key, 'utf-8')

        digestmod = None
        if sign_method == 'HmacSHA256':
            digestmod = hashlib.sha256
        elif sign_method == 'HmacSHA1':
            digestmod = hashlib.sha1
        else:
            raise SDKException("signMethod invalid", "signMethod only support (HmacSHA1, HmacSHA256)")

        hashed = hmac.new(secret_key, sign_str, digestmod)
        base64 = binascii.b2a_base64(hashed.digest())[:-1]

        if sys.version_info[0] > 2:
            base64 = base64.decode()

        return base64