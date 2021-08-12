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


def _threaded(conn: socket, debug: bool):
    while True:
        buffer = conn.recv(4)
        protocol = NewServerProtocol(buffer, 0)
        err = protocol.decode()
        if err.code != 200:
            print(err.message)
            break

        buffer = conn.recv(protocol.length)
        handler = NewServerHandle(protocol.type, buffer)
        response = handler.dispatch()

        protocol = NewServerProtocol(response.data, response.type)
        protocol.encode()
        response = protocol.buffer

        err = conn.sendall(response)
        if err:
            print(err)
        break

    conn.close()


class Server:
    def __init__(self, fd: str, debug: bool = False):
        self.fd = fd.replace("unix:", "")
        self.debug = debug
        if os.path.exists(self.fd):
            os.remove(self.fd)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.fd)
        self.sock.listen(1024)
        print("listening on unix:%s" % self.fd)

    def receive(self):
        while True:
            conn, address = self.sock.accept()

            NewThread(target=_threaded, args=(conn, self.debug)).start()

    def __del__(self):
        self.sock.close()
        os.remove(self.fd)
        print("Bye")
