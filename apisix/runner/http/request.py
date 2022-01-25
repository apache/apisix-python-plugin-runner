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
        self._err_code = 0
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

    def _init(self) -> None:
        """
        init request handler
        :return:
        """
        if self.rpc_type == runner_utils.RPC_HTTP_REQ_CALL:
            req = HCReq.Req.GetRootAsReq(self.rpc_buf)

            # fetch request id
            self.id = req.Id()

            # fetch request conf token
            self.conf_token = req.ConfToken()

            # fetch request uri
            self.path = req.Path().decode()

            # fetch request method
            self.method = runner_utils.get_method_name_by_code(req.Method())

            # fetch request remote_addr
            ip_list = runner_utils.parse_list_vector(req, runner_utils.VECTOR_TYPE_SOURCE_IP, True)
            if ip_list:
                if len(ip_list) == 16:
                    self.src_ip = IPv6Address(bytes(ip_list)).exploded
                else:
                    self.src_ip = IPv4Address(bytes(ip_list)).exploded

            # fetch request headers
            hdr_dict = runner_utils.parse_dict_vector(req, runner_utils.VECTOR_TYPE_HEADER)
            if hdr_dict:
                self.headers = hdr_dict

            # fetch request args
            arg_dict = runner_utils.parse_dict_vector(req, runner_utils.VECTOR_TYPE_QUERY)
            if arg_dict:
                self.args = arg_dict

        if self.rpc_type == runner_utils.RPC_PREPARE_CONF:
            req = PCReq.Req.GetRootAsReq(self.rpc_buf)
            if req.ConfIsNone():
                return

            # loading plugin
            plugins = runner_plugin.loading()
            configs = {}
            for i in range(req.ConfLength()):
                name = str(req.Conf(i).Name().decode()).lower()
                plugin = plugins.get(name)
                if not plugin:
                    continue
                value = req.Conf(i).Value().decode()
                plugin = plugin()
                plugin.config = json.loads(value)
                configs[name] = plugin
            self.configs = configs

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
        return self._err_code
