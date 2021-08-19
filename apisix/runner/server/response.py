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

from a6pluginproto.Err import Code as A6ErrCode

RESP_STATUS_CODE_OK = 200
RESP_STATUS_MESSAGE_OK = "OK"
RESP_STATUS_CODE_BAD_REQUEST = A6ErrCode.Code.BAD_REQUEST
RESP_STATUS_MESSAGE_BAD_REQUEST = "Bad Request"
RESP_STATUS_CODE_SERVICE_UNAVAILABLE = A6ErrCode.Code.SERVICE_UNAVAILABLE
RESP_STATUS_CODE_CONF_TOKEN_NOT_FOUND = A6ErrCode.Code.CONF_TOKEN_NOT_FOUND


class Response:
    def __init__(self, code: int = 0, message: str = '', data: bytes = b'', ty: int = 0):
        """
        init response handler
        :param code:
            response code
        :param message:
            response message
        :param data:
            response data
        :param ty:
            response type
        """
        self.__code = code
        self.__message = message
        self.__type = ty
        self.__data = data

    def __eq__(self, response) -> bool:
        """
        compare response handler
        :param response:
            response handler
        :return:
        """
        return (
                self.code == response.code and self.message == response.message and self.data == response.data and
                self.type == response.type)

    @property
    def code(self) -> int:
        """
        get code by response handler
        :return:
        """
        return self.__code

    @property
    def message(self) -> str:
        """
        get message by response handler
        :return:
        """
        return self.__message

    @property
    def data(self) -> bytes:
        """
        get data by response handler
        :return:
        """
        return self.__data

    @property
    def type(self) -> int:
        """
        get type by response handler
        :return:
        """
        return self.__type
