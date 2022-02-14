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
    resp.set_req_id(1)
    ok = resp.call_handler(builder)
    assert not ok
    resp.set_body("Hello Python Runner")
    ok = resp.call_handler(builder)
    assert ok


def test_response_handler():
    resp = RunnerHttpResponse()
    resp.set_header("X-HELLO", "Python")
    assert resp.get_headers() == {"X-HELLO": "Python"}
    resp.set_body("Hello, Python")
    assert resp.get_body() == "Hello, Python"
    resp.set_req_id(1000)
    assert resp.get_req_id() == 1000
    resp.set_status_code(200)
    assert resp.get_status_code() == 200
