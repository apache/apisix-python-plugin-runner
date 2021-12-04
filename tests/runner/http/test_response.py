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

import apisix.runner.utils.common as runner_utils
from apisix.runner.http.response import Response as RunnerHttpResponse


def test_response_call_handler():
    builder = runner_utils.new_builder()
    resp = RunnerHttpResponse()
    ok = resp.call_handler(builder)
    assert not ok
    resp.body = "Hello Python Runner"
    ok = resp.call_handler(builder)
    assert ok


def test_response_handler():
    resp = RunnerHttpResponse()
    resp.rpc_type = runner_utils.RPC_UNKNOWN
    assert resp.rpc_type == runner_utils.RPC_UNKNOWN
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
