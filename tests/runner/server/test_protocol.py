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

from apisix.runner.server.protocol import Protocol as NewServerProtocol
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from apisix.runner.server.response import RESP_STATUS_CODE_OK
from apisix.runner.server.response import RESP_STATUS_MESSAGE_OK


def test_protocol_encode():
    buf_str = "Hello Python Runner".encode()
    protocol = NewServerProtocol(buffer=buf_str, ty=RPC_PREPARE_CONF)
    err = protocol.encode()
    buf_len = len(buf_str)
    buf_arr = bytearray(buf_len.to_bytes(4, byteorder="big"))
    buf_arr[0] = RPC_PREPARE_CONF
    buf_data = bytes(buf_arr) + buf_str
    buf_len = len(buf_data)
    assert err.code == RESP_STATUS_CODE_OK
    assert err.message == RESP_STATUS_MESSAGE_OK
    assert protocol.type == RPC_PREPARE_CONF
    assert protocol.buffer == buf_data
    assert protocol.length == buf_len


def test_protocol_decode():
    buf_str = "Hello Python Runner".encode()
    buf_len = len(buf_str)
    buf_arr = bytearray(buf_len.to_bytes(4, byteorder="big"))
    buf_arr[0] = RPC_PREPARE_CONF
    buf_data = bytes(buf_arr)
    protocol = NewServerProtocol(buffer=buf_data)
    err = protocol.decode()
    assert err.code == RESP_STATUS_CODE_OK
    assert err.message == RESP_STATUS_MESSAGE_OK
    assert protocol.type == RPC_PREPARE_CONF
    assert protocol.length == buf_len
