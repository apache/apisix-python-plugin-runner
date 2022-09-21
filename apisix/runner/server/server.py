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

from pwd import getpwnam
from threading import Thread as NewThread
from apisix.runner.server.handle import Handle as NewServerHandle
from apisix.runner.server.protocol import Protocol as NewServerProtocol
from apisix.runner.server.config import Config as NewServerConfig
from apisix.runner.server.logger import Logger as NewServerLogger
from apisix.runner.server.response import RESP_STATUS_CODE_OK

PROTOCOL_HEADER_LEN = 4


class RPCData:
    def __init__(self, ty: int = 0, data: bytes = b''):
        self.ty = ty
        self.data = data


class RPCRequest:
    def __init__(self, conn: socket.socket, log: NewServerLogger):
        self.conn = conn
        self.log = log
        self.request = RPCData()
        self.response = RPCData()


def _threaded(r: RPCRequest):
    while True:
        try:
            buffer = r.conn.recv(PROTOCOL_HEADER_LEN)
            protocol = NewServerProtocol(buffer, 0)
            err = protocol.decode()
            if err.code != RESP_STATUS_CODE_OK:
                r.log.error(err.message)
                break

            r.request.ty = protocol.type
            r.log.info("request type:{}, len:{}", protocol.type, protocol.length)

            r.request.data = r.conn.recv(protocol.length)
            handler = NewServerHandle(r)
            response = handler.dispatch()
            protocol = NewServerProtocol(response.Output(), protocol.type)
            protocol.encode()

            r.log.info("response type:{}, len:{}", protocol.type, protocol.length)

            r.conn.sendall(protocol.buffer)
        except socket.timeout as e:
            r.log.info("connection timout: {}", e.args.__str__())
            break
        except socket.error as e:
            r.log.error("connection error: {}", e.args.__str__())
            break

    r.conn.close()
    del r


class Server:
    def __init__(self, config: NewServerConfig):
        self.fd = config.socket.file
        if os.path.exists(self.fd):
            os.remove(self.fd)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.fd)
        user = getpwnam(config.socket.owner)
        os.chown(self.fd, user.pw_uid, user.pw_gid)
        self.sock.listen(1024)

        self.logger = NewServerLogger(config.logging.level)

        print("listening on unix:%s" % self.fd)

    def receive(self):
        while True:
            conn, address = self.sock.accept()
            conn.settimeout(60)

            r = RPCRequest(conn, self.logger)
            thread = NewThread(target=_threaded, args=(r,))
            thread.setDaemon(True)
            thread.start()

    def __del__(self):
        self.sock.close()
        os.remove(self.fd)
        print("Bye")
