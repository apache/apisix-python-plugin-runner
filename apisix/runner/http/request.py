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
import json
from ipaddress import IPv4Address
from ipaddress import IPv6Address
import apisix.runner.plugin.core as RunnerPlugin
import apisix.runner.http.method as RunnerMethod
from apisix.runner.http.protocol import RPC_HTTP_REQ_CALL
from apisix.runner.http.protocol import RPC_PREPARE_CONF
from a6pluginproto.HTTPReqCall import Req as A6HTTPReqCallReq
from a6pluginproto.PrepareConf import Req as A6PrepareConfReq


class Request:

    def __init__(self, ty: int = 0, buf: bytes = b''):
        """
        Init and parse request
        :param ty:
            rpc request protocol type
        :param buf:
            rpc request buffer data
        """
        self._rpc_type = ty
        self._rpc_buf = buf
        self._req_id = 0
        self._req_conf_token = 0
        self._req_method = ""
        self._req_path = ""
        self._req_headers = {}
        self._req_configs = {}
        self._req_args = {}
        self._req_src_ip = ""
        self._init()

    @property
    def rpc_type(self) -> int:
        """
        get request protocol type for request handler
        :return:
        """
        return self._rpc_type

    @rpc_type.setter
    def rpc_type(self, rpc_type: int) -> None:
        """
        set request protocol type for request handler
        :param rpc_type:
        :return:
        """
        self._rpc_type = rpc_type

    @property
    def rpc_buf(self) -> bytes:
        """
        get request buffer data for request handler
        :return:
        """
        return self._rpc_buf

    @rpc_buf.setter
    def rpc_buf(self, rpc_buf: bytes) -> None:
        """
        set request buffer data for request handler
        :return:
        """
        self._rpc_buf = rpc_buf

    @property
    def conf_token(self) -> int:
        """
        get request token for request handler
        :return:
        """
        return self._req_conf_token

    @conf_token.setter
    def conf_token(self, req_conf_token: int) -> None:
        """
        set request token for request handler
        :return:
        """
        self._req_conf_token = req_conf_token

    @property
    def id(self) -> int:
        """
        get request id for request handler
        :return:
        """
        return self._req_id

    @id.setter
    def id(self, req_id: int) -> None:
        """
        set request id for request handler
        :return:
        """
        self._req_id = req_id

    @property
    def method(self) -> str:
        """
        get request method for request handler
        :return:
        """
        return self._req_method

    @method.setter
    def method(self, req_method: str) -> None:
        """
        set request method for request handler
        :return:
        """
        self._req_method = req_method

    @property
    def path(self) -> str:
        """
        get request path for request handler
        :return:
        """
        return self._req_path

    @path.setter
    def path(self, req_path: str) -> None:
        """
        set request path for request handler
        :return:
        """
        self._req_path = req_path

    @property
    def headers(self) -> dict:
        """
        get request headers for request handler
        :return:
        """
        return self._req_headers

    @headers.setter
    def headers(self, req_headers: dict) -> None:
        """
        set request headers for request handler
        :return:
        """
        self._req_headers = req_headers

    @property
    def configs(self) -> dict:
        """
        get plugin instance and configs for request handler
        :return:
        """
        return self._req_configs

    @configs.setter
    def configs(self, req_configs: dict) -> None:
        """
        set plugin instance and configs for request handler
        :return:
        """
        self._req_configs = req_configs

    @property
    def args(self) -> dict:
        """
        get request args for request handler
        :return:
        """
        return self._req_args

    @args.setter
    def args(self, req_args: dict) -> None:
        """
        set request args for request handler
        :return:
        """
        self._req_args = req_args

    @property
    def src_ip(self) -> str:
        """
        get request source ip address for request handler
        :return:
        """
        return self._req_src_ip

    @src_ip.setter
    def src_ip(self, req_src_ip: str) -> None:
        """
        set request source ip address for request handler
        :return:
        """
        self._req_src_ip = req_src_ip

    def reset(self) -> None:
        """
        reset request handler
        :return:
        """
        """
        reset request class
        :return:
        """
        self._rpc_type = 0
        self._rpc_buf = b''
        self._req_id = 0
        self._req_conf_token = 0
        self._req_method = ""
        self._req_path = ""
        self._req_headers = {}
        self._req_configs = {}
        self._req_args = {}
        self._req_src_ip = ""

    def _parse_src_ip(self, req: A6HTTPReqCallReq) -> None:
        """
        parse request source ip address
        :param req:
        :return:
        """
        if req.SrcIpIsNone():
            return
        ip_len = req.SrcIpLength()
        if ip_len == 0:
            return
        ip_arr = bytearray()
        for i in range(ip_len):
            ip_arr.append(req.SrcIp(i))
        ip_byte = bytes(ip_arr)

        if ip_len == 4:
            self.src_ip = IPv4Address(ip_byte).exploded
        if ip_len == 16:
            self.src_ip = IPv6Address(ip_byte).exploded

    def _parse_headers(self, req: A6HTTPReqCallReq) -> None:
        """
        parse request headers
        :param req:
        :return:
        """
        if not req.HeadersIsNone():
            headers = {}
            for i in range(req.HeadersLength()):
                key = str(req.Headers(i).Name(), encoding="UTF-8")
                val = str(req.Headers(i).Value(), encoding="UTF-8")
                headers[key] = val
            self.headers = headers

    def _parse_args(self, req: A6HTTPReqCallReq) -> None:
        """
        parse request args
        :param req:
        :return:
        """
        if not req.ArgsIsNone():
            args = {}
            for i in range(req.ArgsLength()):
                key = str(req.Args(i).Name(), encoding="UTF-8")
                val = str(req.Args(i).Value(), encoding="UTF-8")
                args[key] = val
            self.args = args

    def _parse_configs(self, req: A6PrepareConfReq) -> None:
        """
        parse request plugin configs
        :param req:
        :return:
        """
        if not req.ConfIsNone():
            plugins = RunnerPlugin.loading()
            configs = {}
            for i in range(req.ConfLength()):
                name = str(req.Conf(i).Name(), encoding="UTF-8").lower()
                plugin = plugins.get(name)
                if not plugin:
                    continue
                value = str(req.Conf(i).Value(), encoding="UTF-8")
                plugin = plugin()
                plugin.config = json.loads(value)
                configs[name] = plugin
            self.configs = configs

    def _init(self) -> None:
        """
        init request handler
        :return:
        """
        if self.rpc_type == RPC_HTTP_REQ_CALL:
            req = A6HTTPReqCallReq.Req.GetRootAsReq(self.rpc_buf)
            self.id = req.Id()
            self.method = RunnerMethod.get_name_by_code(req.Method())
            self.path = str(req.Path(), encoding="UTF-8")
            self.conf_token = req.ConfToken()
            self._parse_src_ip(req)
            self._parse_headers(req)
            self._parse_args(req)

        if self.rpc_type == RPC_PREPARE_CONF:
            req = A6PrepareConfReq.Req.GetRootAsReq(self.rpc_buf)
            self._parse_configs(req)
