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
import runner.socket.handle as RunnerSocketHandle
import runner.socket.protocol as RunnerSocketProtocol


def threaded(conn):
    while True:
        buffer = conn.recv(4)
        protocol = RunnerSocketProtocol.New(buffer, 0)
        err = protocol.decode()
        if err.code() != 200:
            print(err.message())
            break

        buffer = conn.recv(protocol.length())
        handler = RunnerSocketHandle.New(protocol.type(), buffer)
        response = handler.dispatch()

        protocol = RunnerSocketProtocol.New(response.data(), response.type())
        protocol.encode()
        response = protocol.buffer()

        err = conn.sendall(response)
        if err:
            print(err)
        break

    conn.close()


class New:
    def __init__(self, socket_address):
        if os.path.exists(socket_address):
            os.remove(socket_address)
        self.socket_address = socket_address
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(socket_address)
        self.sock.listen(1024)
        print("listening on unix:%s" % socket_address)

    def receive(self):
        while True:
            conn, address = self.sock.accept()

            NewThread(target=threaded, args=(conn,)).start()

    def __del__(self):
        self.sock.close()
        print("Bye")
