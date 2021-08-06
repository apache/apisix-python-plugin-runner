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
import runner.plugin.cache as RunnerPluginCache
import runner.plugin.execute as RunnerPluginExecute
import runner.http.request as RunnerHttpRequest
import runner.http.response as RunnerHttpResponse
import runner.http.protocol as RunnerHttpProtocol
import runner.socket.error as RunnerSocketError


class New(object):

    def __init__(self, ty: int = 0, buf: bytes = b''):
        self.__buffer = buf
        self.__type = ty

    def __rpc_config(self) -> RunnerSocketError:
        # init request
        req = RunnerHttpRequest.Request(RunnerHttpProtocol.RPC_PREPARE_CONF, self.__buffer)
        # generate token
        token = RunnerPluginCache.generateToken()
        # get plugins config
        configs = req.getConfigs()
        # cache plugins config
        ok = RunnerPluginCache.setConfigByToken(token, configs)
        if not ok:
            return RunnerSocketError.New(A6ErrCode.Code.SERVICE_UNAVAILABLE, "cache token failure")
        # init response
        reps = RunnerHttpResponse.Response(RunnerHttpProtocol.RPC_PREPARE_CONF)
        response = reps.setToken(token).responseToFlatBuffers()

        return RunnerSocketError.New(code=RunnerSocketError.RUNNER_SUCCESS_CODE, message="OK", data=response.Output(),
                                     ty=self.__type)

    def __rpc_call(self) -> RunnerSocketError:
        # init request
        req = RunnerHttpRequest.Request(RunnerHttpProtocol.RPC_HTTP_REQ_CALL, self.__buffer)
        # get request token
        token = req.getConfToken()
        # get plugins
        configs = RunnerPluginCache.getConfigByToken(token)
        if len(configs) == 0:
            return RunnerSocketError.New(A6ErrCode.Code.CONF_TOKEN_NOT_FOUND, "cache token not found")
        # init response
        reps = RunnerHttpResponse.Response(RunnerHttpProtocol.RPC_HTTP_REQ_CALL)
        # execute plugins
        RunnerPluginExecute.executeFilter(configs, req, reps)

        response = reps.responseToFlatBuffers()
        return RunnerSocketError.New(code=RunnerSocketError.RUNNER_SUCCESS_CODE, message="OK", data=response.Output(),
                                     ty=self.__type)

    def __rpc_test(self) -> RunnerSocketError:
        # init response
        reps = RunnerHttpResponse.Response(RunnerHttpProtocol.RPC_TEST)
        reps.setBody("Hello, Python Runner of APISIX")
        response = reps.responseToFlatBuffers()
        return RunnerSocketError.New(code=RunnerSocketError.RUNNER_SUCCESS_CODE, message="OK", data=response.Output(),
                                     ty=self.__type)

    @staticmethod
    def __rpc_unknown(err_code: int = 0) -> RunnerSocketError:
        resp = RunnerHttpResponse.Response(RunnerHttpProtocol.RPC_ERROR)
        resp.setErrorCode(err_code)
        response = resp.responseToFlatBuffers()
        return RunnerSocketError.New(code=RunnerSocketError.RUNNER_SUCCESS_CODE, message="OK", data=response.Output(),
                                     ty=RunnerHttpProtocol.RPC_ERROR)

    def dispatch(self) -> RunnerSocketError:
        err = None

        if self.__type == RunnerHttpProtocol.RPC_PREPARE_CONF:
            err = self.__rpc_config()

        if self.__type == RunnerHttpProtocol.RPC_HTTP_REQ_CALL:
            err = self.__rpc_call()

        if self.__type == RunnerHttpProtocol.RPC_TEST:
            err = self.__rpc_test()

        if not err:
            return self.__rpc_unknown()

        size = len(err.data())
        if (size > RunnerHttpResponse.RESP_MAX_DATA_SIZE or size <= 0) and err.code() == 200:
            err = RunnerSocketError.New(A6ErrCode.Code.SERVICE_UNAVAILABLE,
                                        "the max length of data is %d but got %d" % (
                                            RunnerHttpResponse.RESP_MAX_DATA_SIZE, size))
        if err.code() != 200:
            print("ERR: %s" % err.message())
            err = self.__rpc_unknown(err.code())
        return err
