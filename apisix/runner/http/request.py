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
import flatbuffers
import apisix.runner.plugin.core as runner_plugin
import apisix.runner.utils.common as runner_utils

from ipaddress import IPv4Address
from ipaddress import IPv6Address
from A6.HTTPReqCall import Rewrite as HCRw
from A6.HTTPReqCall import Action as HCAction
from A6.HTTPReqCall import Req as HCReq
from A6.PrepareConf import Req as PCReq


class Request:

    def __init__(self, r):
        """
        Init and parse request
        :param r:
            rpc request object
        """
        self._rpc_type = r.request.ty
        self._rpc_buf = r.request.data
        self._req_id = 0
        self.code = 0
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

    def _parse_src_ip(self, req: HCReq) -> None:
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

    def _parse_headers(self, req: HCReq) -> None:
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

    def _parse_args(self, req: HCReq) -> None:
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

    def _parse_configs(self, req: PCReq) -> None:
        """
        parse request plugin configs
        :param req:
        :return:
        """
        if not req.ConfIsNone():
            plugins = runner_plugin.loading()
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
        if self.rpc_type == runner_utils.RPC_HTTP_REQ_CALL:
            req = HCReq.Req.GetRootAsReq(self.rpc_buf)
            self.id = req.Id()
            self.method = runner_utils.get_method_name_by_code(req.Method())
            self.path = str(req.Path(), encoding="UTF-8")
            self.conf_token = req.ConfToken()
            self._parse_src_ip(req)
            self._parse_headers(req)
            self._parse_args(req)

        if self.rpc_type == runner_utils.RPC_PREPARE_CONF:
            req = PCReq.Req.GetRootAsReq(self.rpc_buf)
            self._parse_configs(req)

    def checked(self):
        """
        check request params is valid
        :return:
        """
        if len(self._req_path) == 0 and len(self._req_headers) == 0 and len(self._req_args) == 0:
            return False
        else:
            return True

    @runner_utils.response_config
    def config_handler(self, builder: flatbuffers.Builder):
        return self.conf_token

    @runner_utils.response_call(HCAction.Action.Rewrite)
    def call_handler(self, builder: flatbuffers.Builder):
        if not self.checked():
            return None, 0

        if len(self._req_path) <= 0:
            self._req_path = "/"
        path_vector = runner_utils.create_str_vector(builder, self._req_path)

        headers_vector = runner_utils.create_dict_vector(builder, self._req_headers, HCAction.Action.Rewrite,
                                                         runner_utils.VECTOR_TYPE_HEADER)

        args_vector = runner_utils.create_dict_vector(builder, self._req_args, HCAction.Action.Rewrite,
                                                      runner_utils.VECTOR_TYPE_QUERY)

        HCRw.RewriteStart(builder)
        HCRw.RewriteAddPath(builder, path_vector)
        HCRw.RewriteAddHeaders(builder, headers_vector)
        HCRw.RewriteAddArgs(builder, args_vector)
        rewrite = HCRw.RewriteEnd(builder)
        return rewrite, self._req_id

    @runner_utils.response_unknown
    def unknown_handler(self, builder: flatbuffers.Builder):
        return self.code
