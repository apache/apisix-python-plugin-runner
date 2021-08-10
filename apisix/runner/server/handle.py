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
from __future__ import annotations
from a6pluginproto.Err import Code as A6ErrCode
import apisix.runner.plugin.core as RunnerPlugin
import apisix.runner.plugin.cache as RunnerCache
from apisix.runner.http.response import Response as NewHttpResponse
from apisix.runner.http.response import RESP_MAX_DATA_SIZE
from apisix.runner.http.request import Request as NewHttpRequest
from apisix.runner.server.response import Response as NewServerResponse
from apisix.runner.server.response import RUNNER_SUCCESS_CODE
from apisix.runner.server.response import RUNNER_SUCCESS_MESSAGE
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL
from apisix.runner.http.protocol import RPC_UNKNOWN


class Handle:

    def __init__(self, ty: int = 0, buf: bytes = b'', debug: bool = False):
        """
        Init Python runner server
        :param ty:
            rpc request protocol type
        :param buf:
            rpc request buffer data
        :param debug:
            enable debug mode
        """
        self.type = ty
        self.buffer = buf
        self.debug = debug

    @property
    def type(self) -> int:
        return self._type

    @type.setter
    def type(self, ty: int = 0) -> None:
        self._type = ty

    @property
    def buffer(self) -> bytes:
        return self._buffer

    @buffer.setter
    def buffer(self, buf: bytes = b'') -> None:
        self._buffer = buf

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, debug: bool = False) -> None:
        self._debug = debug

    def _rpc_config(self) -> NewServerResponse:
        # init request
        req = NewHttpRequest(RPC_PREPARE_CONF, self.buffer)
        # generate token
        token = RunnerCache.generate_token()
        # get plugins config
        configs = req.configs
        # cache plugins config
        ok = RunnerCache.set_config_by_token(token, configs)
        if not ok:
            return NewServerResponse(code=A6ErrCode.Code.SERVICE_UNAVAILABLE, message="cache token failure")
        # init response
        resp = NewHttpResponse(RPC_PREPARE_CONF)
        resp.token = token
        response = resp.flatbuffers()

        return NewServerResponse(code=RUNNER_SUCCESS_CODE, message=RUNNER_SUCCESS_MESSAGE, data=response.Output(),
                                 ty=self.type)

    def _rpc_call(self) -> NewServerResponse:
        # init request
        req = NewHttpRequest(RPC_HTTP_REQ_CALL, self.buffer)
        # get request token
        token = req.conf_token
        # get plugins
        configs = RunnerCache.get_config_by_token(token)
        if len(configs) == 0:
            return NewServerResponse(code=A6ErrCode.Code.CONF_TOKEN_NOT_FOUND, message="cache token not found")
        # init response
        resp = NewHttpResponse(RPC_HTTP_REQ_CALL)
        # execute plugins
        RunnerPlugin.filter(configs, req, resp)

        response = resp.flatbuffers()
        return NewServerResponse(code=RUNNER_SUCCESS_CODE, message=RUNNER_SUCCESS_MESSAGE, data=response.Output(),
                                 ty=self.type)

    @staticmethod
    def _rpc_unknown(err_code: int = 0) -> NewServerResponse:
        resp = NewHttpResponse(RPC_UNKNOWN)
        resp.error_code = err_code
        response = resp.flatbuffers()
        return NewServerResponse(code=RUNNER_SUCCESS_CODE, message="OK", data=response.Output(),
                                 ty=RPC_UNKNOWN)

    def dispatch(self) -> NewServerResponse:
        err = None

        if self.type == RPC_PREPARE_CONF:
            err = self._rpc_config()

        if self.type == RPC_HTTP_REQ_CALL:
            err = self._rpc_call()

        if not err:
            return self._rpc_unknown()

        size = len(err.data)
        if (size > RESP_MAX_DATA_SIZE or size <= 0) and err.code == 200:
            err = NewServerResponse(A6ErrCode.Code.SERVICE_UNAVAILABLE,
                                    "the max length of data is %d but got %d" % (
                                        RESP_MAX_DATA_SIZE, size))
        if err.code != 200:
            print("ERR: %s" % err.message)
            err = self._rpc_unknown(err.code)
        return err
