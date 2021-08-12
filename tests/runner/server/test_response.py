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

from apisix.runner.server.response import Response as NewServerResponse
from apisix.runner.server.response import RUNNER_ERROR_CODE
from apisix.runner.server.response import RUNNER_SUCCESS_CODE
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL
from apisix.runner.http.protocol import RPC_UNKNOWN


def test_response_code():
    response = NewServerResponse(code=RUNNER_SUCCESS_CODE)
    assert response.code == RUNNER_SUCCESS_CODE
    error = NewServerResponse(code=RUNNER_ERROR_CODE)
    assert error.code == RUNNER_ERROR_CODE


def test_response_message():
    response = NewServerResponse(message="Hello Python Runner")
    assert response.message == "Hello Python Runner"


def test_response_data():
    response = NewServerResponse(data="Hello Python Runner".encode())
    assert response.data == b'Hello Python Runner'


def test_response_type():
    response = NewServerResponse(ty=RPC_UNKNOWN)
    assert response.type == RPC_UNKNOWN
    response = NewServerResponse(ty=RPC_PREPARE_CONF)
    assert response.type == RPC_PREPARE_CONF
    response = NewServerResponse(ty=RPC_HTTP_REQ_CALL)
    assert response.type == RPC_HTTP_REQ_CALL


def test_response_eq():
    resp1 = NewServerResponse(code=RUNNER_SUCCESS_CODE, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    resp2 = NewServerResponse(code=RUNNER_ERROR_CODE, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    resp3 = NewServerResponse(code=RUNNER_SUCCESS_CODE, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    assert resp1 != resp2
    assert resp1 == resp3
