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
from _thread import start_new_thread
from runner.socket.handle import Handle as A6ServerHandle


def runner_protocol_decode(buf):
    """
    decode for runner protocol
    :param buf:
    :return:
    """
    if not buf:
        return None, "runner protocol undefined."
    if len(buf) != 4:
        return None, "runner protocol invalid."

    buf = bytearray(buf)
    # request buf type
    buf_type = buf[0]
    buf[0] = 0
    # request buf length
    buf_len = int.from_bytes(buf, byteorder="big")
    return {"type": buf_type, "len": buf_len}, None


def runner_protocol_encode(reps_type, reps_data):
    """
    encode for runner protocol
    :param reps_type:
    :param reps_data:
    :return:
    """
    reps_len = len(reps_data)
    reps_header = reps_len.to_bytes(4, byteorder="big")
    reps_header = bytearray(reps_header)
    reps_header[0] = reps_type
    reps_header = bytes(reps_header)
    return reps_header + reps_data


def threaded(conn):
    while True:
        header_buf = conn.recv(4)
        protocol, err = runner_protocol_decode(header_buf)
        if err:
            print(err)
            break

        # rpc request type
        req_type = protocol.get("type")
        # rpc request length
        req_len = protocol.get("len")

        req_data = conn.recv(req_len)

        rpc_handler = A6ServerHandle(req_type, req_data)
        response = rpc_handler.dispatch()

        reps_type = response.get("type")
        reps_data = response.get("data")
        reps = runner_protocol_encode(reps_type, reps_data)

        err = conn.sendall(reps)
        if err:
            print(err)
            break
    conn.close()


class Server:
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

            start_new_thread(threaded, (conn,))

    def __del__(self):
        self.sock.close()
        print("Bye")
