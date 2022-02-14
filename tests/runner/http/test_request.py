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
    req.set_conf_token(0)
    ok = req.config_handler(builder)
    assert not ok
    req.set_conf_token(1)
    ok = req.config_handler(builder)
    assert ok


def test_request_call_handler():
    builder = runner_utils.new_builder()
    r = default_request()
    req = RunnerHttpRequest(r)
    req.set_uri("")
    req.set_headers({})
    req.set_args({})
    ok = req.call_handler(builder)
    assert not ok
    req.set_header("X-Hello", "World")
    req.set_id(1)
    ok = req.call_handler(builder)
    assert ok
    req.set_uri("/hello")
    req.set_id(1)
    ok = req.call_handler(builder)
    assert ok


def test_request_handler():
    r = default_request()
    req = RunnerHttpRequest(r)
    req.set_id(10)
    assert req.get_id() == 10
    req.set_conf_token(10)
    assert req.get_conf_token() == 10
    req.set_method("GET")
    assert req.get_method() == "GET"
    req.set_uri("/hello")
    assert req.get_uri() == "/hello"
    req.set_headers({"X-HELLO": "Python"})
    assert req.get_headers() == {"X-HELLO": "Python"}
    req.set_config("hello", "Python")
    assert req.get_configs() == {"hello": "Python"}
    req.set_args({"hello": "Python"})
    assert req.get_args() == {"hello": "Python"}
