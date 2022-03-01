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
    default_key = "hello"
    default_val = "world"
    default_empty_str = ""
    default_empty_dict = {}
    default_id = 1000
    default_token = 1
    default_uri = "/hello"
    default_method = "GET"
    default_ip = "127.0.0.1"

    r = default_request()
    req = RunnerHttpRequest(r)

    assert not req.set_id(0)
    assert req.set_id(default_id)
    assert req.get_id() == default_id

    assert not req.set_conf_token(0)
    assert req.set_conf_token(default_token)
    assert req.get_conf_token() == default_token

    assert not req.set_method(default_key)
    assert req.set_method(default_method)
    assert req.get_method() == default_method

    assert not req.set_uri(default_key)
    assert req.set_uri(default_uri)
    assert req.get_uri() == default_uri

    assert not req.set_header(default_key, default_empty_str)
    assert req.set_header(default_key, default_val)
    assert req.get_header(default_key) == default_val

    assert not req.set_headers(default_empty_dict)
    assert req.set_headers({default_key: default_val})
    assert req.get_headers() == {default_key: default_val}

    assert not req.set_config(default_empty_str, default_empty_str)
    assert req.set_config(default_key, default_empty_str)
    assert req.set_config(default_key, default_val)
    assert req.get_config(default_key) == default_val

    assert not req.set_configs(default_empty_dict)
    assert req.set_configs({default_key: default_val})
    assert req.get_configs() == {default_key: default_val}

    assert not req.set_arg(default_key, default_empty_str)
    assert req.set_arg(default_key, default_val)
    assert req.get_arg(default_key) == default_val

    assert not req.set_args(default_empty_dict)
    assert req.set_args({default_key: default_val})
    assert req.get_args() == {default_key: default_val}

    assert not req.set_remote_addr(default_empty_str)
    assert req.set_remote_addr(default_ip)
    assert req.get_remote_addr() == default_ip

    assert not req.set_body(default_empty_str)
    assert req.get_body() == default_empty_str
    assert req.set_body(default_val)
    assert req.get_body() == default_val

    assert not req.set_var(default_key, default_empty_str)
    assert req.get_var(default_key) == default_empty_str
    assert req.set_var(default_key, default_val)
    assert req.get_var(default_key) == default_val
