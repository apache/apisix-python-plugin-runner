#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import flatbuffers
import apisix.runner.utils.common as runner_utils
from A6.HTTPReqCall import Stop as HCStop
from A6.HTTPReqCall import Action as HCAction

RESP_MAX_DATA_SIZE = 2 << 24 - 1

PLUGIN_ACTION_STOP = HCAction.Action.Stop
PLUGIN_ACTION_REWRITE = HCAction.Action.Rewrite


class Response:

    def __init__(self):
        """
        Init and parse request
        """

        # response attribute
        self.__body = ""
        self.__headers = {}
        self.__status_code = 0

        # custom attribute
        self.__req_id = 0

    def get_header(self, key: str) -> str:
        """
        get response header
        :param key:
        :return:
        """
        return self.__headers.get(key)

    def set_header(self, key: str, value: str) -> bool:
        """
        set response header
        :param key:
        :param value:
        :return:
        """
        if key and value:
            self.__headers[key] = value
            return True
        return False

    def get_headers(self) -> dict:
        """
        get response headers
        :return:
        """
        return self.__headers

    def set_headers(self, headers: dict) -> bool:
        """
        get response headers
        :param headers:
        :return:
        """
        if headers:
            self.__headers = headers
            return True
        return False

    def get_body(self) -> str:
        """
        get response body
        :return:
        """
        return self.__body

    def set_body(self, body: str) -> bool:
        """
        get response body
        :return:
        """
        if body:
            self.__body = body
            return True
        return False

    def get_status_code(self) -> int:
        """
        get response status code
        :return:
        """
        return self.__status_code or 200

    def set_status_code(self, status_code: int) -> bool:
        """
        set response status code
        :param status_code:
        :return:
        """
        if status_code and (100 <= status_code <= 599):
            self.__status_code = status_code
            return True
        return False

    def get_req_id(self) -> int:
        """
        get request id
        :return:
        """
        return self.__req_id

    def set_req_id(self, req_id: int) -> bool:
        """
        set request id
        :param req_id:
        :return:
        """
        if req_id:
            self.__req_id = req_id
            return True
        return False

    def changed(self) -> bool:
        """
        check response handler is change
        :return:
        """
        if self.__body or self.__headers or self.__status_code:
            return True
        else:
            return False

    @runner_utils.response_call(HCAction.Action.Stop)
    def call_handler(self, builder: flatbuffers.Builder):
        """
        get http call response
        :param builder:
        :return:
        """
        if not self.changed():
            return None, 0
        headers_vector = runner_utils.create_dict_vector(builder, self.get_headers(), HCAction.Action.Stop,
                                                         runner_utils.VECTOR_TYPE_HEADER)

        body_vector = runner_utils.create_str_vector(builder, self.get_body())

        status_code = self.get_status_code()

        HCStop.StopStart(builder)
        HCStop.StopAddStatus(builder, status_code)
        HCStop.StopAddBody(builder, body_vector)
        HCStop.StopAddHeaders(builder, headers_vector)
        stop = HCStop.StopEnd(builder)
        return stop, self.get_req_id()
