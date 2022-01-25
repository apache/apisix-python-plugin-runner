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
import logging
import socket

import apisix.runner.utils.common as runner_utils
from apisix.runner.server.handle import Handle as RunnerServerHandle
from apisix.runner.server.logger import Logger as RunnerServerLogger
from apisix.runner.server.server import RPCRequest as RunnerRPCRequest
from A6.HTTPReqCall import Req as A6HTTPReqCallReq
from A6.PrepareConf import Req as A6PrepareConfReq
from A6.PrepareConf import Resp as A6PrepareConfResp
from A6 import TextEntry as A6TextEntry
from A6 import Method as A6Method
from A6.Err.Resp import Resp as ErrResp
from A6.HTTPReqCall.Resp import Resp as HCResp
from A6.HTTPReqCall.Action import Action as HCAction
from A6.Err.Code import Code as ErrCode
from A6.HTTPReqCall.Stop import Stop as HCStop
from A6.HTTPReqCall.Rewrite import Rewrite as HCRewrite


def default_request():
    sock = socket.socket()
    logger = RunnerServerLogger(logging.INFO)
    return RunnerRPCRequest(sock, logger)


def default_plugin_buffer(name: str = "stop", enable_conf: bool = True):
    builder = runner_utils.new_builder()
    conf = 0
    if enable_conf:
        name = builder.CreateString(name)
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
    return builder.Output()


def default_call_buffer(token: int = 0, id: int = 1, ipv6: bool = False):
    builder = runner_utils.new_builder()
    # request path
    path = builder.CreateString("/hello/python/runner")
    # request ip
    if ipv6:
        src_ip = bytes(bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]))
    else:
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
    A6HTTPReqCallReq.AddId(builder, id)
    A6HTTPReqCallReq.AddMethod(builder, A6Method.Method.GET)
    A6HTTPReqCallReq.AddPath(builder, path)
    A6HTTPReqCallReq.AddSrcIp(builder, src_ip)
    A6HTTPReqCallReq.AddArgs(builder, args_vec)
    A6HTTPReqCallReq.AddHeaders(builder, headers_vec)
    A6HTTPReqCallReq.AddConfToken(builder, token)
    req = A6HTTPReqCallReq.End(builder)
    builder.Finish(req)
    return builder.Output()


def test_dispatch_unknown():
    r = default_request()
    r.request.ty = runner_utils.RPC_UNKNOWN
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    err = ErrResp.GetRootAsResp(response.Output())
    assert err.Code() == ErrCode.BAD_REQUEST


def test_dispatch_config():
    buf = default_plugin_buffer("stop", False)
    r = default_request()
    r.request.ty = runner_utils.RPC_PREPARE_CONF
    r.request.data = buf
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    err = ErrResp.GetRootAsResp(response.Output())
    assert err.Code() == ErrCode.BAD_REQUEST

    buf = default_plugin_buffer("stop")
    r.request.ty = runner_utils.RPC_PREPARE_CONF
    r.request.data = buf
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    resp = A6PrepareConfResp.Resp.GetRootAs(response.Output())
    assert resp.ConfToken() != 0


def test_dispatch_call():
    r = default_request()
    r.request.ty = runner_utils.RPC_PREPARE_CONF
    r.request.data = default_plugin_buffer("stop")
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    resp = A6PrepareConfResp.Resp.GetRootAs(response.Output())
    assert resp.ConfToken() != 0

    buf = default_call_buffer(resp.ConfToken())
    r.request.ty = runner_utils.RPC_HTTP_REQ_CALL
    r.request.data = buf
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    resp = HCResp.GetRootAsResp(response.Output())
    assert resp.Id() > 0
    assert resp.ActionType() == HCAction.Stop
    stop = HCStop()
    stop.Init(resp.Action().Bytes, resp.Action().Pos)
    assert stop.BodyLength() == len("Hello, Python Runner of APISIX")
    assert stop.Status() == 201

    r.request.ty = runner_utils.RPC_PREPARE_CONF
    r.request.data = default_plugin_buffer("rewrite")
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    resp = A6PrepareConfResp.Resp.GetRootAs(response.Output())
    assert resp.ConfToken() != 0
    conf_token = resp.ConfToken()
    r.request.ty = runner_utils.RPC_HTTP_REQ_CALL
    r.request.data = default_call_buffer(conf_token)
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    resp = HCResp.GetRootAsResp(response.Output())
    assert resp.Id() > 0
    assert resp.ActionType() == HCAction.Rewrite
    rewrite = HCRewrite()
    rewrite.Init(resp.Action().Bytes, resp.Action().Pos)
    assert rewrite.Path() == b'/a6/python/runner'

    r.request.data = default_call_buffer(conf_token, ipv6=True)
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    resp = HCResp.GetRootAsResp(response.Output())
    assert resp.Id() > 0
    assert resp.ActionType() == HCAction.Rewrite

    r.request.ty = runner_utils.RPC_HTTP_REQ_CALL
    r.request.data = default_call_buffer(conf_token, 0)
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    resp = ErrResp.GetRootAs(response.Output())
    assert resp.Code() == ErrCode.BAD_REQUEST

    r.request.data = default_call_buffer()
    handle = RunnerServerHandle(r)
    response = handle.dispatch()
    reps = ErrResp.GetRootAs(response.Output())
    assert reps.Code() == ErrCode.BAD_REQUEST
