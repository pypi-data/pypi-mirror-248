# Copyright (c) 2018 Ltd.
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
from enginefaas.common.exception.sdk_exception import SDKException
from enginefaas.common.profile.http_profile import HttpProfile


class ClientProfile(object):
    unsignedPayload = False

    def __init__(self, signMethod=None, httpProfile=None, language="zh-CN",
                 disable_region_breaker=True, region_breaker_profile=None):
        """SDK profile.

        :param signMethod: The signature method, valid choice: HmacSHA1, HmacSHA256, TC3-HMAC-SHA256
        :type signMethod: str
        :param httpProfile: The http profile
        :type httpProfile: :class:`HttpProfile`
        :param language: Valid choice: en-US, zh-CN.
        :type language: str
        :param disable_region_breaker: Switch of region breaker.
        :type disable_region_breaker: bool
        :param region_breaker_profile: The region breaker profile.
        :type region_breaker_profile: :class:`RegionBreakerProfile`
        """
        self.httpProfile = HttpProfile() if httpProfile is None else httpProfile
        self.signMethod = "HmacSHA256" if signMethod is None else signMethod
        valid_language = ["zh-CN", "en-US"]
        if language not in valid_language:
            raise SDKException("ClientError", "Language invalid, choices: %s" % valid_language)
        self.language = language
