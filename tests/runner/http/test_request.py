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

import socket
import logging
import apisix.runner.utils.common as runner_utils
from apisix.runner.server.logger import Logger as RunnerServerLogger
from apisix.runner.server.server import RPCRequest as RunnerRPCRequest
from apisix.runner.http.request import Request as RunnerHttpRequest


def default_request():
    sock = socket.socket()
    logger = RunnerServerLogger(logging.INFO)
    return RunnerRPCRequest(sock, logger)


def test_request_unknown_handler():
    builder = runner_utils.new_builder()
    r = default_request()
    req = RunnerHttpRequest(r)
    ok = req.unknown_handler(builder)
    assert ok


def test_request_config_handler():
    builder = runner_utils.new_builder()
    r = default_request()
    req = RunnerHttpRequest(r)
    req.conf_token = 0
    ok = req.config_handler(builder)
    assert not ok
    req.conf_token = 1
    ok = req.config_handler(builder)
    assert ok


def test_request_call_handler():
    builder = runner_utils.new_builder()
    r = default_request()
    req = RunnerHttpRequest(r)
    req.path = ""
    req.headers = {}
    req.args = {}
    ok = req.call_handler(builder)
    assert not ok
    req.path = "/hello"
    ok = req.call_handler(builder)
    assert ok


def test_request_handler():
    r = default_request()
    req = RunnerHttpRequest(r)
    req.id = 1000
    assert req.id == 1000
    req.rpc_type = runner_utils.RPC_UNKNOWN
    assert req.rpc_type == runner_utils.RPC_UNKNOWN
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
