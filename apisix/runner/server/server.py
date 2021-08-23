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

from threading import Thread as NewThread
from apisix.runner.server.handle import Handle as NewServerHandle
from apisix.runner.server.protocol import Protocol as NewServerProtocol
from apisix.runner.server.config import Config as NewServerConfig
from apisix.runner.server.logger import Logger as NewServerLogger
from apisix.runner.server.response import RESP_STATUS_CODE_OK

logger = NewServerLogger()


def _threaded(conn: socket.socket):
    while True:
        try:
            buffer = conn.recv(4)
            protocol = NewServerProtocol(buffer, 0)
            err = protocol.decode()
            if err.code != RESP_STATUS_CODE_OK:
                logger.error(err.message)
                break

            logger.info("request type:{}, len:{}", protocol.type, protocol.length)

            buffer = conn.recv(protocol.length)
            handler = NewServerHandle(protocol.type, buffer)
            response = handler.dispatch()
            if response.code != RESP_STATUS_CODE_OK:
                logger.error(response.message)

            protocol = NewServerProtocol(response.data, response.type)
            protocol.encode()

            logger.info("response type:{}, len:{}", protocol.type, protocol.length)

            conn.sendall(protocol.buffer)
        except socket.timeout as e:
            logger.info("connection timout: {}", e.args.__str__())
            break
        except socket.error as e:
            logger.error("connection error: {}", e.args.__str__())
            break

    conn.close()


class Server:
    def __init__(self, config: NewServerConfig):
        self.fd = config.socket.file
        if os.path.exists(self.fd):
            os.remove(self.fd)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.fd)
        self.sock.listen(1024)

        logger.set_level(config.logging.level)
        print("listening on unix:%s" % self.fd)

    def receive(self):
        while True:
            conn, address = self.sock.accept()
            conn.settimeout(60)

            thread = NewThread(target=_threaded, args=(conn,))
            thread.setDaemon(True)
            thread.start()

    def __del__(self):
        self.sock.close()
        os.remove(self.fd)
        print("Bye")
