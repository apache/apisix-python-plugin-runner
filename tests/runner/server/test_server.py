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
from pwd import struct_passwd
import socket
import logging
from unittest.mock import patch
from apisix.runner.server.server import Server as RunnerServer
from apisix.runner.server.server import RPCRequest as RunnerRPCRequest
from apisix.runner.server.logger import Logger as RunnerServerLogger
from apisix.runner.server.config import Config as RunnerConfig

@patch('pwd.getpwnam', return_value=struct_passwd({"pw_name":"nobody", "pw_passwd":"x", "pw_uid":65534, "pw_gid":65534, "pw_gecos":"nobody", "pw_dir":"/", "pw_shell":"/sbin/nologin"}))
@patch('os.chown')
def test_server(mock_chown,mock_getpwnam,capsys):
    config = RunnerConfig("%s" % os.path.abspath(os.path.join(os.getcwd(),"tests")), "config.yaml")
    server = RunnerServer(config)
    mock_chown.assert_called_with("/tmp/runner.sock",65534,65534)
    del server
    captured = capsys.readouterr()
    assert captured.out.find("listening on unix") != -1
    assert captured.out.find("Bye") != -1


def test_rpc_request():
    sock = socket.socket()
    logger = RunnerServerLogger(logging.INFO)
    r = RunnerRPCRequest(sock, logger)
    assert r.log == logger
    assert r.conn == sock
    assert r.request.ty == 0
    assert len(r.request.data) == 0
