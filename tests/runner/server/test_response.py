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
from apisix.runner.server.response import RESP_STATUS_CODE_BAD_REQUEST
from apisix.runner.server.response import RESP_STATUS_CODE_SERVICE_UNAVAILABLE
from apisix.runner.server.response import RESP_STATUS_CODE_CONF_TOKEN_NOT_FOUND
from apisix.runner.server.response import RESP_STATUS_CODE_OK
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL
from apisix.runner.http.protocol import RPC_UNKNOWN


def test_response_code():
    resp = NewServerResponse(code=RESP_STATUS_CODE_OK)
    assert resp.code == RESP_STATUS_CODE_OK
    resp = NewServerResponse(code=RESP_STATUS_CODE_BAD_REQUEST)
    assert resp.code == RESP_STATUS_CODE_BAD_REQUEST
    resp = NewServerResponse(code=RESP_STATUS_CODE_SERVICE_UNAVAILABLE)
    assert resp.code == RESP_STATUS_CODE_SERVICE_UNAVAILABLE
    resp = NewServerResponse(code=RESP_STATUS_CODE_CONF_TOKEN_NOT_FOUND)
    assert resp.code == RESP_STATUS_CODE_CONF_TOKEN_NOT_FOUND


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
    resp1 = NewServerResponse(code=RESP_STATUS_CODE_OK, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    resp2 = NewServerResponse(code=RESP_STATUS_CODE_BAD_REQUEST, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    resp3 = NewServerResponse(code=RESP_STATUS_CODE_OK, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    assert resp1 != resp2
    assert resp1 == resp3
