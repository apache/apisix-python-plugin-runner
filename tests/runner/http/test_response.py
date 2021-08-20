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

from apisix.runner.http.response import Response as NewHttpResponse
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.http.protocol import RPC_UNKNOWN
from a6pluginproto.PrepareConf.Resp import Resp as PrepareConfResp
from a6pluginproto.HTTPReqCall.Resp import Resp as HTTPReqCallResp
from a6pluginproto.HTTPReqCall.Action import Action as HTTPReqCallAction
from a6pluginproto.HTTPReqCall.Stop import Stop as HTTPReqCallStop
from a6pluginproto.HTTPReqCall.Rewrite import Rewrite as HTTPReqCallRewrite
from a6pluginproto.Err.Code import Code as A6ErrCode
from a6pluginproto.Err.Resp import Resp as A6ErrResp


def test_response_config():
    token = 1
    resp = NewHttpResponse(ty=RPC_PREPARE_CONF)
    resp.token = token
    response = resp.flatbuffers()
    flat_resp = PrepareConfResp.GetRootAs(response.Output())
    assert resp.changed()
    assert flat_resp.ConfToken() == token


def test_response_call():
    headers = {
        "X-TEST-HELLO": "hello",
        "X-TEST-WORLD": "world"
    }
    args = {
        "A-TEST-HELLO": "hello",
        "A-TEST-WORLD": "world",
    }
    body = "hello world"
    resp = NewHttpResponse(ty=RPC_HTTP_REQ_CALL)
    resp.headers = headers
    resp.body = body
    resp.status_code = 200
    resp.action_type = HTTPReqCallAction.Stop
    response = resp.flatbuffers()
    flat_resp = HTTPReqCallResp.GetRootAs(response.Output())
    assert resp.changed()
    assert flat_resp.ActionType() == HTTPReqCallAction.Stop
    action = flat_resp.Action()
    stop = HTTPReqCallStop()
    stop.Init(action.Bytes, action.Pos)
    body_list = []
    body_len = stop.BodyLength()
    for i in range(body_len):
        body_list.append(chr(stop.Body(i)))
    assert "".join(body_list) == body
    header_dict = {}
    header_len = stop.HeadersLength()
    for j in range(header_len):
        entry = stop.Headers(j)
        hk = str(entry.Name(), encoding="utf-8")
        hv = str(entry.Value(), encoding="utf-8")
        header_dict[hk] = hv
    assert header_dict.get("X-TEST-HELLO") == headers.get("X-TEST-HELLO")
    assert header_dict.get("X-TEST-WORLD") == headers.get("X-TEST-WORLD")
    assert stop.Status() == resp.status_code

    resp = NewHttpResponse(ty=RPC_HTTP_REQ_CALL)
    resp.headers = headers
    resp.args = args
    resp.path = "/hello/runner"
    resp.action_type = HTTPReqCallAction.Rewrite
    response = resp.flatbuffers()
    flat_resp = HTTPReqCallResp.GetRootAs(response.Output())
    assert resp.changed()
    assert flat_resp.ActionType() == HTTPReqCallAction.Rewrite
    action = flat_resp.Action()
    rewrite = HTTPReqCallRewrite()
    rewrite.Init(action.Bytes, action.Pos)
    args_dict = {}
    args_len = rewrite.ArgsLength()
    for k in range(args_len):
        entry = rewrite.Args(k)
        ak = str(entry.Name(), encoding="utf-8")
        av = str(entry.Value(), encoding="utf-8")
        args_dict[ak] = av
    assert args_dict.get("A-TEST-HELLO") == args.get("A-TEST-HELLO")
    assert args_dict.get("A-TEST-WORLD") == args.get("A-TEST-WORLD")
    header_dict = {}
    header_len = rewrite.HeadersLength()
    for j in range(header_len):
        entry = rewrite.Headers(j)
        hk = str(entry.Name(), encoding="utf-8")
        hv = str(entry.Value(), encoding="utf-8")
        header_dict[hk] = hv
    assert header_dict.get("X-TEST-HELLO") == headers.get("X-TEST-HELLO")
    assert header_dict.get("X-TEST-WORLD") == headers.get("X-TEST-WORLD")
    assert rewrite.Path().decode(encoding="UTF-8") == resp.path


def test_response_unknown():
    resp = NewHttpResponse(ty=RPC_UNKNOWN)
    resp.error_code = A6ErrCode.BAD_REQUEST
    response = resp.flatbuffers()
    flat_resp = A6ErrResp.GetRootAs(response.Output())
    assert flat_resp.Code() == A6ErrCode.BAD_REQUEST


def test_response_handler():
    resp = NewHttpResponse()
    resp.rpc_type = RPC_UNKNOWN
    assert resp.rpc_type == RPC_UNKNOWN
    resp.token = 1000
    assert resp.token == 1000
    resp.headers = {"X-HELLO": "Python"}
    assert resp.headers == {"X-HELLO": "Python"}
    resp.body = "Hello, Python"
    assert resp.body == "Hello, Python"
    resp.args = {"hello": "Python"}
    assert resp.args == {"hello": "Python"}
    resp.path = "/hello"
    assert resp.path == "/hello"
    resp.id = 1000
    assert resp.id == 1000
    resp.status_code = 200
    assert resp.status_code == 200
    resp.error_code = 1
    assert resp.error_code == 1
    resp.action_type = 10
    assert resp.action_type == 10
    resp.reset()
    assert resp.rpc_type == 0
    assert resp.id == 0
    assert resp.token == 0
    assert resp.body == ""
    assert resp.path == ""
    assert resp.args == {}
    assert resp.headers == {}
    assert resp.status_code == 0
    assert resp.error_code == 0
    assert resp.action_type == 0
