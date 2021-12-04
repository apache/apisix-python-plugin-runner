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

    def __init__(self, ty: int = 0):
        """
        Init and parse request
        :param ty:
            rpc request protocol type
        """
        self.rpc_type = ty
        self._resp_id = 0
        self._resp_token = 0
        self._resp_body = ""
        self._resp_path = ""
        self._resp_args = {}
        self._resp_headers = {}
        self._resp_status_code = 0
        self._resp_error_code = 0
        self._resp_action_type = 0

    @property
    def rpc_type(self) -> int:
        """
        get protocol type for response handler
        :return:
        """
        return self._rpc_type

    @rpc_type.setter
    def rpc_type(self, rpc_type: int) -> None:
        """
        set protocol type for response handler
        :return:
        """
        self._rpc_type = rpc_type

    @property
    def id(self) -> int:
        """
        get request id for response handler
        :return:
        """
        return self._resp_id

    @id.setter
    def id(self, resp_id: int) -> None:
        """
        set request id for response handler
        :return:
        """
        self._resp_id = resp_id

    @property
    def token(self) -> int:
        """
        get token for response handler
        :return:
        """
        return self._resp_token

    @token.setter
    def token(self, resp_token: int) -> None:
        """
        set token for response handler
        :return:
        """
        self._resp_token = resp_token

    @property
    def body(self) -> str:
        """
        get body for response handler
        :return:
        """
        return self._resp_body

    @body.setter
    def body(self, resp_body: str) -> None:
        """
        set body for response handler
        :return:
        """
        self._resp_body = resp_body

    @property
    def path(self) -> str:
        """
        get path for response handler
        :return:
        """
        return self._resp_path

    @path.setter
    def path(self, resp_path: str) -> None:
        """
        set path for response handler
        :return:
        """
        self._resp_path = resp_path

    @property
    def args(self) -> dict:
        """
        get args for response handler
        :return:
        """
        return self._resp_args

    @args.setter
    def args(self, resp_args: dict) -> None:
        """
        set args for response handler
        :return:
        """
        self._resp_args = resp_args

    @property
    def headers(self) -> dict:
        """
        get headers for response handler
        :return:
        """
        return self._resp_headers

    @headers.setter
    def headers(self, resp_headers: dict) -> None:
        """
        set headers for response handler
        :return:
        """
        self._resp_headers = resp_headers

    @property
    def status_code(self) -> int:
        """
        get status code for response handler
        :return:
        """
        return self._resp_status_code

    @status_code.setter
    def status_code(self, resp_status_code: int) -> None:
        """
        set status code for response handler
        :return:
        """
        self._resp_status_code = resp_status_code

    @property
    def error_code(self) -> int:
        """
        get error code for response handler
        :return:
        """
        return self._resp_error_code

    @error_code.setter
    def error_code(self, resp_error_code: int = 0) -> None:
        """
        set error code for response handler
        :return:
        """
        self._resp_error_code = resp_error_code

    @property
    def action_type(self):
        """
        get action type for response handler
        :return:
        """
        return self._resp_action_type

    @action_type.setter
    def action_type(self, action_type: int = 0) -> None:
        """
        set action type for response handler
        :param action_type:
        :return:
        """
        self._resp_action_type = action_type

    def reset(self) -> None:
        """
        reset response handler
        :return:
        """
        self._rpc_type = 0
        self._resp_id = 0
        self._resp_token = 0
        self._resp_body = ""
        self._resp_path = ""
        self._resp_args = {}
        self._resp_headers = {}
        self._resp_status_code = 0
        self._resp_error_code = 0
        self._resp_action_type = 0

    def changed(self) -> bool:
        """
        check response handler is change
        :return:
        """
        if self.body or self.headers or self.status_code or self.token or self.error_code:
            return True
        else:
            return False

    @runner_utils.response_call(HCAction.Action.Stop)
    def call_handler(self, builder: flatbuffers.Builder):
        if not self.changed():
            return None, 0
        headers_vector = runner_utils.create_dict_vector(builder, self.headers, HCAction.Action.Stop,
                                                         runner_utils.VECTOR_TYPE_HEADER)

        body_vector = runner_utils.create_str_vector(builder, self.body)

        status_code = 200
        if self.status_code > 0:
            status_code = self.status_code

        HCStop.StopStart(builder)
        HCStop.StopAddStatus(builder, status_code)
        HCStop.StopAddBody(builder, body_vector)
        HCStop.StopAddHeaders(builder, headers_vector)
        stop = HCStop.StopEnd(builder)
        return stop, self.id
