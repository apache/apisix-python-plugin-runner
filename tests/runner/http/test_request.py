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

from apisix.runner.http.request import Request as NewHttpRequest
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL
from apisix.runner.http.protocol import RPC_UNKNOWN
from apisix.runner.http.protocol import new_builder
from apisix.runner.http.method import get_name_by_code
from apisix.runner.plugin.core import loading
from a6pluginproto.HTTPReqCall import Req as A6HTTPReqCallReq
from a6pluginproto.PrepareConf import Req as A6PrepareConfReq
from a6pluginproto import TextEntry as A6TextEntry
from a6pluginproto import Method as A6Method


def _create_entry(builder: flatbuffers.Builder, name: str, value: str) -> int:
    name = builder.CreateString(name)
    value = builder.CreateString(value)
    A6TextEntry.Start(builder)
    A6TextEntry.AddName(builder, name)
    A6TextEntry.AddValue(builder, value)
    return A6TextEntry.End(builder)


def test_request_config():
    builder = new_builder()
    plugins = loading()
    conf_data = 0
    for name in plugins:
        conf_data = _create_entry(builder, name, '{"runner":"Python"}')
        break
    A6PrepareConfReq.ReqStartConfVector(builder, 1)
    builder.PrependUOffsetTRelative(conf_data)
    conf = builder.EndVector()
    A6PrepareConfReq.Start(builder)
    A6PrepareConfReq.AddConf(builder, conf)
    req = A6PrepareConfReq.End(builder)
    builder.Finish(req)
    buf = builder.Output()
    req = NewHttpRequest(ty=RPC_PREPARE_CONF, buf=buf)
    assert req.configs
    assert len(req.configs) >= 1


def test_request_call():
    req_path = "/hello/python/runner"
    req_src_ip = [127, 0, 0, 1]
    req_args = {"a": "args"}
    req_headers = {"h": "headers"}

    builder = new_builder()
    path = builder.CreateString(req_path)
    src_ip = bytes(bytearray(req_src_ip))
    src_ip = builder.CreateByteVector(src_ip)

    args = _create_entry(builder, "a", req_args.get("a"))
    A6HTTPReqCallReq.StartArgsVector(builder, 1)
    builder.PrependUOffsetTRelative(args)
    args_vec = builder.EndVector()

    headers = _create_entry(builder, "h", req_headers.get("h"))
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
    req = NewHttpRequest(ty=RPC_HTTP_REQ_CALL, buf=buf)

    assert req.src_ip == ".".join('%s' % ip for ip in req_src_ip)
    assert req.path == req_path
    assert req.args.get("a") == req_args.get("a")
    assert req.headers.get("h") == req_headers.get("h")
    assert req.method == get_name_by_code(A6Method.Method.GET)


def test_request_handler():
    req = NewHttpRequest()
    req.id = 1000
    assert req.id == 1000
    req.rpc_type = RPC_UNKNOWN
    assert req.rpc_type == RPC_UNKNOWN
    req.rpc_buf = b'hello'
    assert req.rpc_buf == b'hello'
    req.conf_token = 10
    assert req.conf_token == 10
    req.method = "GET"
    assert req.method == "GET"
    req.path = "/hello"
    assert req.path == "/hello"
    req.headers = {"X-HELLO": "Python"}
    assert req.headers == {"X-HELLO": "Python"}
    req.configs = {"hello": "Python"}
    assert req.configs == {"hello": "Python"}
    req.args = {"hello": "Python"}
    assert req.args == {"hello": "Python"}
    req.src_ip = "127.0.0.1"
    assert req.src_ip == "127.0.0.1"
    req.reset()
    assert req.rpc_type == 0
    assert req.rpc_buf == b''
    assert req.id == 0
    assert req.conf_token == 0
    assert req.method == ""
    assert req.path == ""
    assert req.headers == {}
    assert req.configs == {}
    assert req.args == {}
    assert req.src_ip == ""
