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

from apisix.runner.plugin.core import PluginBase
from apisix.runner.plugin.core import PluginProcess
from apisix.runner.plugin.core import PLUGINS
from apisix.runner.server.logger import Logger as RunnerServerLogger
from apisix.runner.server.server import RPCRequest as RunnerRPCRequest
from apisix.runner.http.request import Request as NewHttpRequest
from apisix.runner.http.response import Response as NewHttpResponse


class NonePlugin:
    pass


class ErrorPlugin:

    def config(self, conf):
        return conf

    def filter(self, conf, req, reps):
        raise RuntimeError("Runtime Error")


def default_request():
    sock = socket.socket()
    logger = RunnerServerLogger(logging.INFO)
    return RunnerRPCRequest(sock, logger)


def test_process_register():
    assert PLUGINS == {}
    PluginProcess.register()
    assert len(PLUGINS) == 2


def test_process_execute():
    r = default_request()
    request = NewHttpRequest(r)
    response = NewHttpResponse()
    tests = [
        {
            "conf": {
                "stop": "config"
            },
            "autoload": True,
            "req": request,
            "resp": response,
            "expected": True
        },
        {
            "conf": {
                "rewrite": "config"
            },
            "autoload": True,
            "req": request,
            "resp": response,
            "expected": True
        },
        # AnyError
        {
            "conf": {
                "any": "config"
            },
            "plugins": {
                "any": ErrorPlugin
            },
            "autoload": False,
            "expected": False
        },
        # AttributeError
        {
            "conf": {
                "attr": "config"
            },
            "plugins": {
                "attr": NonePlugin
            },
            "autoload": False,
            "expected": False
        },
        # TypeError
        {
            "conf": {
                "none": "config"
            },
            "autoload": True,
            "expected": False
        },
    ]

    for test in tests:
        if test.get("autoload"):
            PluginProcess.register()
        if test.get("plugins"):
            for plg_name, plg_obj in test.get("plugins").items():
                PLUGINS[plg_name] = plg_obj
        res = PluginProcess.execute(test.get("conf"), r, test.get("req"), test.get("resp"))
        assert res == test.get("expected")


def test_base():
    r = default_request()
    pb = PluginBase()
    assert pb.name() is None
    assert pb.config(None) is None
    assert pb.filter(None, NewHttpRequest(r), NewHttpResponse()) is None
