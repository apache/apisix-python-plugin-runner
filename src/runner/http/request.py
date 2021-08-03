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
import json
import runner.http.method as RunnerHttpMethod
import runner.http.protocol as RunnerHttpProtocol
import runner.plugin.loading as RunnerPluginLoading
from a6pluginproto.HTTPReqCall import Req as A6HTTPReqCallReq
from a6pluginproto.PrepareConf import Req as A6PrepareConfReq


class Request(object):

    def __init__(self, rpc_type: int, buf: bytes):
        self.request = {}
        self.setRpcType(rpc_type)
        self.initRequest(buf)

    def setRpcType(self, rpc_type: int) -> None:
        self.request["rpc_type"] = rpc_type

    def getRpcType(self) -> int:
        return self.request.get("rpc_type", 0)

    def setConfToken(self, conf_token: int) -> None:
        self.request["conf_token"] = conf_token

    def getConfToken(self) -> int:
        return self.request.get("conf_token", 0)

    def getId(self) -> int:
        return self.request.get("id", 0)

    def setId(self, id: int) -> None:
        self.request["id"] = id

    def getMethod(self) -> str:
        return self.request.get("method", "")

    def setMethod(self, method: str) -> None:
        self.request["method"] = method

    def getPath(self) -> str:
        return self.request.get("path", "")

    def setPath(self, path: str) -> None:
        self.request["path"] = path

    def setHeaders(self, headers: dict) -> None:
        self.request["headers"] = headers

    def getHeaders(self) -> dict:
        return self.request.get("headers", {})

    def setConfigs(self, headers: dict) -> None:
        self.request["configs"] = headers

    def getConfigs(self) -> dict:
        return self.request.get("configs", {})

    def setArgs(self, args: dict) -> None:
        self.request["args"] = args

    def getArgs(self) -> dict:
        return self.request.get("args", {})

    def getSourceIP(self) -> str:
        return self.request.get("src_ip", "")

    def setSourceIP(self, ip: str) -> None:
        self.request["src_ip"] = ip

    def initRequest(self, buf: bytes) -> None:
        if self.getRpcType() == RunnerHttpProtocol.RPC_HTTP_REQ_CALL:
            req = A6HTTPReqCallReq.Req.GetRootAsReq(buf)
            self.setId(req.Id())
            self.setMethod(RunnerHttpMethod.getNameByCode(req.Method()))
            self.setPath(str(req.Path(), encoding="UTF-8"))
            self.setConfToken(req.ConfToken())

            if not req.SrcIpIsNone():
                delimiter = "."
                if req.SrcIpLength() > 4:
                    delimiter = ":"
                ipAddress = []
                for i in range(req.SrcIpLength()):
                    ipAddress.append(str(req.SrcIp(i)))
                self.setSourceIP(delimiter.join(ipAddress))

            if not req.HeadersIsNone():
                headers = {}
                for i in range(req.HeadersLength()):
                    key = str(req.Headers(i).Name(), encoding="UTF-8")
                    val = str(req.Headers(i).Value(), encoding="UTF-8")
                    headers[key] = val
                self.setHeaders(headers)

            if not req.ArgsIsNone():
                args = {}
                for i in range(req.ArgsLength()):
                    key = str(req.Args(i).Name(), encoding="UTF-8")
                    val = str(req.Args(i).Value(), encoding="UTF-8")
                    args[key] = val
                self.setArgs(args)

        if self.getRpcType() == RunnerHttpProtocol.RPC_PREPARE_CONF:
            req = A6PrepareConfReq.Req.GetRootAsReq(buf)
            plugins = RunnerPluginLoading.instances()
            configs = {}
            if not req.ConfIsNone():
                for i in range(req.ConfLength()):
                    name = str(req.Conf(i).Name(), encoding="UTF-8").lower()
                    plugin = plugins.get(name)
                    if not plugin:
                        continue
                    value = str(req.Conf(i).Value(), encoding="UTF-8")
                    plugin = plugin()
                    plugin.setConfig(json.loads(value))
                    configs[name] = plugin
                self.setConfigs(configs)
