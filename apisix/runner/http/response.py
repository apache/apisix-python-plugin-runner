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
from a6pluginproto import TextEntry as A6TextEntry
from a6pluginproto.Err import Resp as A6ErrResp
from a6pluginproto.HTTPReqCall import Stop as A6HTTPReqCallStop
from a6pluginproto.HTTPReqCall import Rewrite as A6HTTPReqCallRewrite
from a6pluginproto.HTTPReqCall import Resp as A6HTTPReqCallResp
from a6pluginproto.HTTPReqCall import Action as A6HTTPReqCallAction
from a6pluginproto.PrepareConf import Resp as A6PrepareConfResp
from apisix.runner.http.protocol import new_builder
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL

RESP_MAX_DATA_SIZE = 2 << 24 - 1

PLUGIN_ACTION_STOP = A6HTTPReqCallAction.Action.Stop
PLUGIN_ACTION_REWRITE = A6HTTPReqCallAction.Action.Rewrite


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

    def _gen_config_flat(self, builder: flatbuffers.Builder) -> int:
        A6PrepareConfResp.Start(builder)
        A6PrepareConfResp.AddConfToken(builder, self.token)
        return A6PrepareConfResp.End(builder)

    def _gen_unknown_flat(self, builder: flatbuffers.Builder) -> int:
        A6ErrResp.Start(builder)
        A6ErrResp.AddCode(builder, self.error_code)
        return A6ErrResp.End(builder)

    def _gen_request_flat(self, builder: flatbuffers.Builder) -> int:
        def _to_a6_entry(data: dict) -> list:
            entries = []
            if not isinstance(data, dict) and len(data) <= 0:
                return entries
            for key in data:
                val = data[key]
                key_b = builder.CreateString(key)
                val_b = builder.CreateString(val)
                A6TextEntry.Start(builder)
                A6TextEntry.AddName(builder, key_b)
                A6TextEntry.AddValue(builder, val_b)
                entry = A6TextEntry.End(builder)
                entries.append(entry)
            return entries

        if self.action_type == A6HTTPReqCallAction.Action.Stop:
            headers_entry = _to_a6_entry(self.headers)
            headers_len = len(headers_entry)
            A6HTTPReqCallStop.StopStartHeadersVector(builder, headers_len)
            for i in range(headers_len - 1, -1, -1):
                builder.PrependUOffsetTRelative(headers_entry[i])
            headers_vector = builder.EndVector()

            body = b''
            if self.body and len(self.body) > 0:
                body = self.body.encode(encoding="UTF-8")
            body_vector = builder.CreateByteVector(body)

            status_code = 200
            if self.status_code > 0:
                status_code = self.status_code

            A6HTTPReqCallStop.StopStart(builder)
            A6HTTPReqCallStop.StopAddStatus(builder, status_code)
            A6HTTPReqCallStop.StopAddBody(builder, body_vector)
            A6HTTPReqCallStop.StopAddHeaders(builder, headers_vector)
            action = A6HTTPReqCallStop.StopEnd(builder)
        else:
            args_entry = _to_a6_entry(self.args)
            args_len = len(args_entry)
            A6HTTPReqCallRewrite.RewriteStartArgsVector(builder, args_len)
            for i in range(args_len - 1, -1, -1):
                builder.PrependUOffsetTRelative(args_entry[i])
            args_vector = builder.EndVector()

            headers_entry = _to_a6_entry(self.headers)
            headers_len = len(headers_entry)
            A6HTTPReqCallRewrite.RewriteStartHeadersVector(builder, headers_len)
            for i in range(headers_len - 1, -1, -1):
                builder.PrependUOffsetTRelative(headers_entry[i])
            headers_vector = builder.EndVector()

            path = b'/'
            if self.path and len(self.path) > 0:
                path = self.path.encode(encoding="UTF-8")
            path_vector = builder.CreateByteVector(path)

            A6HTTPReqCallRewrite.RewriteStart(builder)
            A6HTTPReqCallRewrite.RewriteAddPath(builder, path_vector)
            A6HTTPReqCallRewrite.RewriteAddArgs(builder, args_vector)
            A6HTTPReqCallRewrite.RewriteAddHeaders(builder, headers_vector)
            action = A6HTTPReqCallRewrite.RewriteEnd(builder)

        A6HTTPReqCallResp.Start(builder)
        A6HTTPReqCallResp.AddId(builder, self.id)
        A6HTTPReqCallResp.AddActionType(builder, self.action_type)
        A6HTTPReqCallResp.AddAction(builder, action)
        return A6HTTPReqCallResp.End(builder)

    def flatbuffers(self) -> flatbuffers.Builder:
        """
        response to flat buffer object
        :return:
        """
        builder = new_builder()

        rpc_handlers = {
            RPC_PREPARE_CONF: self._gen_config_flat,
            RPC_HTTP_REQ_CALL: self._gen_request_flat
        }

        res = rpc_handlers.get(self.rpc_type, self._gen_unknown_flat)(builder)
        builder.Finish(res)
        return builder
