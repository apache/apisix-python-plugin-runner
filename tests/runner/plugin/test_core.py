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

import os
import socket
import logging
from pkgutil import iter_modules

from apisix.runner.plugin.core import loading as plugin_loading
from apisix.runner.plugin.core import execute as plugin_execute
from apisix.runner.server.logger import Logger as RunnerServerLogger
from apisix.runner.server.server import RPCRequest as RunnerRPCRequest
from apisix.runner.http.request import Request as NewHttpRequest
from apisix.runner.http.response import Response as NewHttpResponse


def test_loading():
    configs = plugin_loading()
    assert isinstance(configs, dict)
    config_keys = configs.keys()
    path = "%s/plugins" % os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    modules = iter_modules(path=[path])
    for _, name, _ in modules:
        assert name in config_keys


def test_execute():
    sock = socket.socket()
    logger = RunnerServerLogger(logging.INFO)
    r = RunnerRPCRequest(sock, logger)
    request = NewHttpRequest(r)
    response = NewHttpResponse()
    configs = plugin_loading()
    for p_name in configs:
        configs[p_name] = configs.get(p_name)()
    ok = plugin_execute(configs, r, request, response)
    assert ok
    # stop plugin
    assert response.headers.get("X-Resp-A6-Runner") == "Python"
    assert response.body == "Hello, Python Runner of APISIX"
    assert response.status_code == 201
    # rewrite plugin
    assert request.headers.get("X-Resp-A6-Runner") == "Python"
    assert request.args.get("a6_runner") == "Python"
    assert request.path == "/a6/python/runner"
    configs = {"test": {}}
    ok = plugin_execute(configs, r, request, response)
    assert not ok

    class AttributeErrorExample:
        pass

    configs = {AttributeErrorExample.__name__.lower(): AttributeErrorExample()}
    ok = plugin_execute(configs, r, request, response)
    assert not ok

    class TypeErrorExample:
        def __init__(self):
            self.filter = 10

    configs = {TypeErrorExample.__name__.lower(): TypeErrorExample()}
    ok = plugin_execute(configs, r, request, response)
    assert not ok
