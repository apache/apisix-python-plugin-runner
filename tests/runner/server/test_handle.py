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

from apisix.runner.server.handle import Handle as NewServerHandle
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL
from apisix.runner.http.protocol import RPC_UNKNOWN
from apisix.runner.http.protocol import new_builder
from apisix.runner.server.response import RESP_STATUS_CODE_OK
from apisix.runner.server.response import RESP_STATUS_MESSAGE_OK
from apisix.runner.server.response import RESP_STATUS_CODE_BAD_REQUEST
from apisix.runner.server.response import RESP_STATUS_MESSAGE_BAD_REQUEST
from apisix.runner.server.response import RESP_STATUS_CODE_CONF_TOKEN_NOT_FOUND
from a6pluginproto.HTTPReqCall import Req as A6HTTPReqCallReq
from a6pluginproto.PrepareConf import Req as A6PrepareConfReq
from a6pluginproto.PrepareConf import Resp as A6PrepareConfResp
from a6pluginproto import TextEntry as A6TextEntry
from a6pluginproto import Method as A6Method


def test_type():
    handle = NewServerHandle(ty=RPC_UNKNOWN)
    assert handle.type == RPC_UNKNOWN
    handle = NewServerHandle(ty=RPC_PREPARE_CONF)
    assert handle.type == RPC_PREPARE_CONF
    handle = NewServerHandle(ty=RPC_HTTP_REQ_CALL)
    assert handle.type == RPC_HTTP_REQ_CALL


def test_buffer():
    handle = NewServerHandle(buf="Hello Python Runner".encode())
    assert handle.buffer == b"Hello Python Runner"


def test_debug():
    handle = NewServerHandle(debug=False)
    assert not handle.debug
    handle = NewServerHandle(debug=True)
    assert handle.debug


def test_dispatch_config():
    builder = new_builder()
    name = builder.CreateString("say")
    value = builder.CreateString('{"body":"Hello Python Runner"}')
    A6TextEntry.Start(builder)
    A6TextEntry.AddName(builder, name)
    A6TextEntry.AddValue(builder, value)
    conf_data = A6TextEntry.End(builder)

    A6PrepareConfReq.ReqStartConfVector(builder, 1)
    builder.PrependUOffsetTRelative(conf_data)
    conf = builder.EndVector()

    A6PrepareConfReq.Start(builder)
    A6PrepareConfReq.AddConf(builder, conf)
    req = A6PrepareConfReq.End(builder)
    builder.Finish(req)
    buf = builder.Output()
    handle = NewServerHandle(ty=RPC_PREPARE_CONF, buf=buf)
    response = handle.dispatch()
    resp = A6PrepareConfResp.Resp.GetRootAs(response.data)
    assert response.code == RESP_STATUS_CODE_OK
    assert response.message == RESP_STATUS_MESSAGE_OK
    assert response.type == RPC_PREPARE_CONF
    assert resp.ConfToken() != 0


def test_dispatch_call():
    builder = new_builder()
    # request path
    path = builder.CreateString("/hello/python/runner")
    # request ip
    src_ip = bytes(bytearray([127, 0, 0, 1]))
    src_ip = builder.CreateByteVector(src_ip)
    # request args
    arg_k = builder.CreateString("hello")
    arg_v = builder.CreateString("world")
    A6TextEntry.Start(builder)
    A6TextEntry.AddName(builder, arg_k)
    A6TextEntry.AddValue(builder, arg_v)
    args = A6TextEntry.End(builder)
    A6HTTPReqCallReq.StartArgsVector(builder, 1)
    builder.PrependUOffsetTRelative(args)
    args_vec = builder.EndVector()
    # request headers
    head_k = builder.CreateString("hello")
    head_v = builder.CreateString("world")
    A6TextEntry.Start(builder)
    A6TextEntry.AddName(builder, head_k)
    A6TextEntry.AddValue(builder, head_v)
    headers = A6TextEntry.End(builder)
    A6HTTPReqCallReq.StartHeadersVector(builder, 1)
    builder.PrependUOffsetTRelative(headers)
    headers_vec = builder.EndVector()

    A6HTTPReqCallReq.Start(builder)
    A6HTTPReqCallReq.AddId(builder, 1)
    A6HTTPReqCallReq.AddMethod(builder, A6Method.Method.GET)
    A6HTTPReqCallReq.AddPath(builder, path)
    A6HTTPReqCallReq.AddSrcIp(builder, src_ip)
    A6HTTPReqCallReq.AddArgs(builder, args_vec)
    A6HTTPReqCallReq.AddHeaders(builder, headers_vec)
    req = A6HTTPReqCallReq.End(builder)
    builder.Finish(req)
    buf = builder.Output()

    handle = NewServerHandle(ty=RPC_HTTP_REQ_CALL, buf=buf)
    response = handle.dispatch()
    assert response.code == RESP_STATUS_CODE_CONF_TOKEN_NOT_FOUND
    assert response.type == RPC_UNKNOWN


def test_dispatch_unknown():
    handle = NewServerHandle(ty=RPC_UNKNOWN)
    response = handle.dispatch()
    assert response.code == RESP_STATUS_CODE_BAD_REQUEST
    assert response.message == RESP_STATUS_MESSAGE_BAD_REQUEST
    assert response.type == RPC_UNKNOWN
