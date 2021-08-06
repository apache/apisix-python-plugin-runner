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
import runner.socket.error as RunnerSocketError


class New(object):

    def __init__(self, buffer: bytes = b'', ty: int = 0):
        self.__buffer = buffer
        self.__type = ty
        self.__length = 0

    def length(self) -> int:
        """
        get buffer length
        :return:
        """
        return self.__length

    def type(self) -> int:
        """
        get protocol type
        :return:
        """
        return self.__type

    def buffer(self) -> bytes:
        """
        get buffer data
        :return:
        """
        return self.__buffer

    def encode(self) -> RunnerSocketError.New:
        """
        encode protocol buffer data
        :return:
        """
        if len(self.__buffer) == 0:
            return RunnerSocketError.New(RunnerSocketError.RUNNER_ERROR_CODE, "ERR: send buffer is empty")
        response_len = len(self.__buffer)
        response_header = response_len.to_bytes(4, byteorder="big")
        response_header = bytearray(response_header)
        response_header[0] = self.__type
        response_header = bytes(response_header)
        self.__buffer = response_header + self.__buffer
        self.__length = len(self.__buffer)
        return RunnerSocketError.New(code=RunnerSocketError.RUNNER_SUCCESS_CODE, message="OK")

    def decode(self) -> RunnerSocketError.New:
        """
        decode protocol buffer data
        :return:
        """
        if len(self.__buffer) == 0:
            return RunnerSocketError.New(RunnerSocketError.RUNNER_ERROR_CODE, "ERR: recv buffer is empty")
        length = len(self.__buffer)
        if length != 4:
            return RunnerSocketError.New(RunnerSocketError.RUNNER_ERROR_CODE,
                                         "ERR: recv protocol type length is 4, got %d" % length)

        buf = bytearray(self.__buffer)
        self.__type = buf[0]
        buf[0] = 0
        self.__length = int.from_bytes(buf, byteorder="big")
        return RunnerSocketError.New(code=RunnerSocketError.RUNNER_SUCCESS_CODE, message="OK")
