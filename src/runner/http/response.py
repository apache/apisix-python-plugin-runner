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
import flatbuffers
import runner.http.protocol as RunnerHttpProtocol
from a6pluginproto import TextEntry as A6TextEntry
from a6pluginproto.HTTPReqCall import Stop as A6HTTPReqCallStop
from a6pluginproto.HTTPReqCall import Resp as A6HTTPReqCallResp
from a6pluginproto.HTTPReqCall import Action as A6HTTPReqCallAction
from a6pluginproto.PrepareConf import Resp as A6PrepareConfResp
from a6pluginproto.Err import Resp as A6ErrResp
from a6pluginproto.Err import Code as A6ErrCode

RESP_MAX_DATA_SIZE = 2 << 24 - 1


class Response(object):

    def __init__(self, rpc_type: int):
        self.response = {}
        self.initResponse()
        self.setRpcType(rpc_type)

    def setRpcType(self, rpc_type: int) -> Response:
        self.response["rpc_type"] = rpc_type
        return self

    def getRpcType(self) -> int:
        return self.response.get("rpc_type", 0)

    def setErrorCode(self, error_code: int) -> Response:
        self.response["error_code"] = error_code
        return self

    def getErrorCode(self) -> int:
        return self.response.get("error_code", A6ErrCode.Code.BAD_REQUEST)

    def setId(self, id: int) -> Response:
        self.response["id"] = id
        return self

    def getId(self) -> int:
        return self.response.get("id", 0)

    def setToken(self, token: int) -> Response:
        self.response["token"] = token
        return self

    def getToken(self) -> int:
        return self.response.get("token", 0)

    def setBody(self, value: str) -> Response:
        self.response["body"] = value
        return self

    def getBody(self) -> str:
        return self.response.get("body", "")

    def getHeaders(self) -> dict:
        return self.response.get("headers", {})

    def setHeader(self, key: str, value: str) -> Response:
        if not self.response.get("headers", None):
            self.response["headers"] = {}
        self.response["headers"][key] = value
        return self

    def getHeader(self, key: str) -> str:
        if not self.response.get("headers", None):
            return ""
        return self.response.get("headers").get(key, "")

    def getStatusCode(self) -> int:
        return self.response.get("statusCode", 0)

    def setStatusCode(self, code: int) -> Response:
        self.response["statusCode"] = code
        return self

    def resetResponse(self) -> None:
        self.initResponse()

    def initResponse(self) -> None:
        self.response = {
            "body": "",
            "headers": {},
            "statusCode": 0,
        }

    def responseHasChange(self) -> bool:
        return self.response.get("body") or \
               self.response.get("headers") or \
               self.response.get("statusCode")

    def responseToFlatBuffers(self) -> flatbuffers.Builder:
        rpcType = self.getRpcType()
        builder = RunnerHttpProtocol.newBuilder()

        if rpcType == RunnerHttpProtocol.RPC_PREPARE_CONF:
            A6PrepareConfResp.Start(builder)
            A6PrepareConfResp.AddConfToken(builder, self.getToken())
            res = A6PrepareConfResp.End(builder)
            builder.Finish(res)
        elif rpcType == RunnerHttpProtocol.RPC_HTTP_REQ_CALL:
            headerVector = None
            headers = self.getHeaders()
            if headers:
                headerEntries = []
                for hk in headers:
                    hv = headers[hk]
                    hkb = builder.CreateString(hk)
                    hvb = builder.CreateString(hv)
                    A6TextEntry.Start(builder)
                    A6TextEntry.AddName(builder, hkb)
                    A6TextEntry.AddValue(builder, hvb)
                    headerEntry = A6TextEntry.End(builder)
                    headerEntries.append(headerEntry)

                headerSize = len(headerEntries)
                A6HTTPReqCallStop.StartHeadersVector(builder, headerSize)
                for i in range(headerSize - 1, -1, -1):
                    builder.PrependUOffsetTRelative(headerEntries[i])
                headerVector = builder.EndVector()

            bodyVector = None
            body = self.getBody()
            if body:
                body = body.encode(encoding="UTF-8")
                bodyVector = builder.CreateByteVector(body)

            statusCode = self.getStatusCode()
            A6HTTPReqCallStop.Start(builder)
            if statusCode == 0:
                A6HTTPReqCallStop.AddStatus(builder, 200)
            else:
                A6HTTPReqCallStop.AddStatus(builder, statusCode)
            if headerVector:
                A6HTTPReqCallStop.AddHeaders(builder, headerVector)
            if bodyVector:
                A6HTTPReqCallStop.AddBody(builder, bodyVector)
            stop = A6HTTPReqCallStop.End(builder)

            A6HTTPReqCallResp.Start(builder)
            A6HTTPReqCallResp.AddId(builder, self.getId())
            A6HTTPReqCallResp.AddActionType(builder, A6HTTPReqCallAction.Action.Stop)
            A6HTTPReqCallResp.AddAction(builder, stop)
            res = A6HTTPReqCallResp.End(builder)
            builder.Finish(res)
        elif rpcType == RunnerHttpProtocol.RPC_TEST:
            body = self.getBody()
            bodyVector = builder.CreateByteVector(body)
            A6HTTPReqCallStop.Start(builder)
            A6HTTPReqCallStop.AddBody(builder, bodyVector)
            stop = A6HTTPReqCallStop.End(builder)

            A6HTTPReqCallResp.Start(builder)
            A6HTTPReqCallResp.AddId(builder, 1)
            A6HTTPReqCallResp.AddActionType(builder, A6HTTPReqCallAction.Action.Stop)
            A6HTTPReqCallResp.AddAction(builder, stop)
            res = A6HTTPReqCallResp.End(builder)
            builder.Finish(res)
        else:
            A6ErrResp.Start(builder)
            A6ErrResp.AddCode(builder, self.getErrorCode())
            res = A6ErrResp.End(builder)
            builder.Finish(res)
        return builder
