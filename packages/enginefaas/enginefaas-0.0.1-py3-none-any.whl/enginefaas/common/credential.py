# -*- coding: utf-8 -*-
# Copyright (c) 2018 Tencent Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import time
try:
    # py3
    import configparser
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    # py2
    import ConfigParser as configparser
    from urllib import urlencode
    from urllib import urlopen

from enginefaas.common.exception.sdk_exception import SDKException

class Credential(object):
    def __init__(self, secret_id, secret_key, token=None):
        """Engine FaaS Credentials.

        :param secret_id: The secret id of your credential.
        :type secret_id: str
        :param secret_key: The secret key of your credential.
        :type secret_key: str
        :param token: The federation token of your credential, if this field
                      is specified, secret_id and secret_key should be set
                      accordingly
        """
        if secret_id is None or secret_id.strip() == "":
            raise SDKException("InvalidCredential", "secret id should not be none or empty")
        if secret_id.strip() != secret_id:
            raise SDKException("InvalidCredential", "secret id should not contain spaces")
        self.secret_id = secret_id

        if secret_key is None or secret_key.strip() == "":
            raise SDKException("InvalidCredential", "secret key should not be none or empty")
        if secret_key.strip() != secret_key:
            raise SDKException("InvalidCredential", "secret key should not contain spaces")
        self.secret_key = secret_key

        self.token = token

    @property
    def secretId(self):
        return self.secret_id

    @property
    def secretKey(self):
        return self.secret_key

class EnvironmentVariableCredential():

    def get_credential(self):
        """EngineFaas EnvironmentVariableCredential.

        :param secret_id: The secret id of your credential, get by environment variable FAAS_SECRET_ID
        :type secret_id: str
        :param secret_key: The secret key of your credential. get by environment variable FAAS_SECRET_KEY
        :type secret_key: str
        """
        self.secret_id = os.environ.get('FAAS_SECRET_ID')
        self.secret_key = os.environ.get('FAAS_SECRET_KEY')

        if self.secret_id is None or self.secret_key is None:
            return None
        if len(self.secret_id) == 0 or len(self.secret_key) == 0:
            return None
        return Credential(self.secret_id, self.secret_key)


class DefaultCredentialProvider(object):
    """EngineFaas DefaultCredentialProvider.

    DefaultCredentialProvider will search credential by order EnvironmentVariableCredential.
    """

    def __init__(self):
        self.cred = None

    def get_credential(self):
        return self.get_credentials()

    def get_credentials(self):
        if self.cred is not None:
            return self.cred

        self.cred = EnvironmentVariableCredential().get_credential()
        if self.cred is not None:
            return self.cred

        raise SDKException("ClientSideError", "no valid credentail.")