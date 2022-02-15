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
    default_key = "hello"
    default_val = "world"
    default_empty_str = ""
    default_empty_dict = {}
    default_num_zero = 0
    default_id = 1000
    default_code = 200

    resp = RunnerHttpResponse()

    assert not resp.set_header(default_key, default_empty_str)
    assert resp.set_header(default_key, default_val)
    assert resp.get_header(default_key) == default_val

    assert not resp.set_headers(default_empty_dict)
    assert resp.set_headers({default_key: default_val})
    assert resp.get_headers() == {default_key: default_val}

    assert not resp.set_body(default_empty_str)
    assert resp.set_body(default_val)
    assert resp.get_body() == default_val

    assert not resp.set_req_id(0)
    assert resp.set_req_id(default_id)
    assert resp.get_req_id() == default_id

    assert not resp.set_status_code(default_num_zero)
    assert resp.set_status_code(default_code)
    assert resp.get_status_code() == default_code
