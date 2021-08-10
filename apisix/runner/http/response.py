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
from a6pluginproto import TextEntry as A6TextEntry
from a6pluginproto.Err import Resp as A6ErrResp
from a6pluginproto.HTTPReqCall import Stop as A6HTTPReqCallStop
from a6pluginproto.HTTPReqCall import Resp as A6HTTPReqCallResp
from a6pluginproto.HTTPReqCall import Action as A6HTTPReqCallAction
from a6pluginproto.PrepareConf import Resp as A6PrepareConfResp
from apisix.runner.http.protocol import new_builder
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL

RESP_MAX_DATA_SIZE = 2 << 24 - 1


class Response:

    def __init__(self, ty: int):
        self.rpc_type = ty
        self._resp_id = 0
        self._resp_token = 0
        self._resp_body = ""
        self._resp_headers = {}
        self._resp_status_code = 0
        self._resp_error_code = 0

    @property
    def rpc_type(self) -> int:
        return self._rpc_type

    @rpc_type.setter
    def rpc_type(self, rpc_type: int) -> None:
        self._rpc_type = rpc_type

    @property
    def id(self) -> int:
        return self._resp_id

    @id.setter
    def id(self, resp_id: int) -> None:
        self._resp_id = resp_id

    @property
    def token(self) -> int:
        return self._resp_token

    @token.setter
    def token(self, resp_token: int) -> None:
        self._resp_token = resp_token

    @property
    def body(self) -> str:
        return self._resp_body

    @body.setter
    def body(self, resp_body: str) -> None:
        self._resp_body = resp_body

    @property
    def headers(self) -> dict:
        return self._resp_headers

    @headers.setter
    def headers(self, resp_headers: dict) -> None:
        self._resp_headers = resp_headers

    @property
    def status_code(self) -> int:
        return self._resp_status_code

    @status_code.setter
    def status_code(self, resp_status_code: int) -> None:
        self._resp_status_code = resp_status_code

    @property
    def error_code(self) -> int:
        return self._resp_error_code

    @error_code.setter
    def error_code(self, resp_error_code: int = 0) -> None:
        self._resp_error_code = resp_error_code

    def reset(self) -> None:
        self._rpc_type = 0
        self._resp_id = 0
        self._resp_token = 0
        self._resp_body = ""
        self._resp_headers = {}
        self._resp_status_code = 0
        self._resp_error_code = 0

    def changed(self) -> bool:
        if self.body or self.headers or self.status_code or self.token or self.error_code:
            return True
        else:
            return False

    def flatbuffers(self) -> flatbuffers.Builder:
        builder = new_builder()
        rpc_type = self.rpc_type

        if rpc_type == RPC_PREPARE_CONF:
            A6PrepareConfResp.Start(builder)
            A6PrepareConfResp.AddConfToken(builder, self.token)
            res = A6PrepareConfResp.End(builder)
            builder.Finish(res)
        elif rpc_type == RPC_HTTP_REQ_CALL:
            header_vector = None
            headers = self.headers
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
                header_vector = builder.EndVector()

            body_vector = None
            body = self.body
            if body:
                body = body.encode(encoding="UTF-8")
                body_vector = builder.CreateByteVector(body)

            status_code = self.status_code
            A6HTTPReqCallStop.Start(builder)
            if status_code == 0:
                A6HTTPReqCallStop.AddStatus(builder, 200)
            else:
                A6HTTPReqCallStop.AddStatus(builder, status_code)
            if header_vector:
                A6HTTPReqCallStop.AddHeaders(builder, header_vector)
            if body_vector:
                A6HTTPReqCallStop.AddBody(builder, body_vector)
            stop = A6HTTPReqCallStop.End(builder)

            A6HTTPReqCallResp.Start(builder)
            A6HTTPReqCallResp.AddId(builder, self.id)
            A6HTTPReqCallResp.AddActionType(builder, A6HTTPReqCallAction.Action.Stop)
            A6HTTPReqCallResp.AddAction(builder, stop)
            res = A6HTTPReqCallResp.End(builder)
            builder.Finish(res)
        else:
            A6ErrResp.Start(builder)
            A6ErrResp.AddCode(builder, self.error_code)
            res = A6ErrResp.End(builder)
            builder.Finish(res)
        return builder
