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
from a6pluginproto.Err import Resp as A6ErrResp
from a6pluginproto.Err import Code as A6ErrCode
import runner.plugin.cache as RunnerPluginCache
import runner.plugin.execute as RunnerPluginExecute
import runner.http.request as RunnerHttpRequest
import runner.http.response as RunnerHttpResponse
import runner.http.protocol as RunnerHttpProtocol


class Handle:

    def __init__(self, req_type, req_data):
        self.req_type = req_type
        self.req_data = req_data

    def RpcPrepareConf(self):
        # init request
        req = RunnerHttpRequest.Request(RunnerHttpProtocol.RPC_PREPARE_CONF, self.req_data)
        # generate token
        token = RunnerPluginCache.generateToken()
        # get plugins config
        configs = req.getConfigs()
        # cache plugins config
        RunnerPluginCache.setConfigByToken(token, configs)
        # init response
        reps = RunnerHttpResponse.Response(RunnerHttpProtocol.RPC_PREPARE_CONF)

        return reps.setToken(token).responseToFlatBuffers()

    def RpcHttpReqCall(self):
        # init request
        req = RunnerHttpRequest.Request(RunnerHttpProtocol.RPC_HTTP_REQ_CALL, self.req_data)
        # get request token
        token = req.getConfToken()
        # get plugins
        configs = RunnerPluginCache.getConfigByToken(token)
        # init response
        reps = RunnerHttpResponse.Response(RunnerHttpProtocol.RPC_HTTP_REQ_CALL)
        # execute plugins
        RunnerPluginExecute.executeFilter(configs, req, reps)

        return reps.responseToFlatBuffers()

    def RpcTest(self):
        pass

    def RpcUnknown(self):
        builder = RunnerHttpProtocol.newBuilder()
        A6ErrResp.Start(builder)
        A6ErrResp.AddCode(builder, A6ErrCode.Code.BAD_REQUEST)
        res = A6ErrResp.End(builder)
        builder.Finish(res)
        return builder

    def dispatch(self):
        handler = {
            RunnerHttpProtocol.RPC_UNKNOWN: self.RpcUnknown,
            RunnerHttpProtocol.RPC_TEST: self.RpcTest,
            RunnerHttpProtocol.RPC_PREPARE_CONF: self.RpcPrepareConf,
            RunnerHttpProtocol.RPC_HTTP_REQ_CALL: self.RpcHttpReqCall,
        }
        return {"type": self.req_type, "data": handler.get(self.req_type, self.RpcUnknown)().Output()}
