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

import socket
import flatbuffers
import apisix.runner.utils.common as runner_utils

from ipaddress import IPv4Address
from ipaddress import IPv6Address
from A6.HTTPReqCall import Rewrite as HCRw
from A6.HTTPReqCall import Action as HCAction
from A6.HTTPReqCall import Req as HCReq
from A6.PrepareConf import Req as PCReq
from A6.Err.Code import Code as A6ErrCode
from A6.ExtraInfo import Var as EIVar
from A6.ExtraInfo import ReqBody as EIBody
from A6.ExtraInfo import Info as EIInfo
from A6.ExtraInfo import Req as EIReq
from A6.ExtraInfo import Resp as EIResp
from apisix.runner.server.protocol import Protocol as RunnerServerProtocol
from apisix.runner.server.response import RESP_STATUS_CODE_OK


class Request:

    def __init__(self, r):
        """
        Init and parse request
        :param r:
            rpc request object
        """
        # request object
        self.r = r

        # request attribute
        self.__remote_addr = ""
        self.__headers = {}
        self.__args = {}
        self.__uri = ""
        self.__method = ""
        self.__vars = {}
        self.__body = ""

        # custom attribute
        self.__conf_token = 0
        self.__id = 0
        self.__configs = {}

        self.__init()

    def get_header(self, key: str) -> str:
        """
        get request header
        :param key:
        :return:
        """
        return self.__headers.get(key)

    def set_header(self, key: str, value: str) -> bool:
        """
        set request header
        :param key:
        :param value:
        :return:
        """
        if key and value:
            self.__headers[key] = value
            return True
        return False

    def get_headers(self) -> dict:
        """
        get request headers
        :return:
        """
        return self.__headers

    def set_headers(self, headers: dict) -> bool:
        """
        get request headers
        :param headers:
        :return:
        """
        if headers:
            self.__headers = headers
            return True
        return False

    def get_var(self, key: str) -> str:
        """
        get nginx variable
        :param key:
        :return:
        """
        if self.__vars.get(key):
            return self.__vars.get(key)
        # generate fetch variable RPC request data
        builder = runner_utils.new_builder()
        var_name = builder.CreateString(key)
        EIVar.Start(builder)
        EIVar.AddName(builder, var_name)
        var_req_data = EIVar.End(builder)
        val = self.__ask_extra_info(builder, EIInfo.Info.Var, var_req_data)
        self.set_var(key, val)
        return val

    def set_var(self, key: str, val: str) -> bool:
        """
        set nginx variable
        :param key:
        :param val:
        :return:
        """
        if key and val:
            self.__vars[key] = val
            return True
        return False

    def get_body(self) -> str:
        """
        get request body
        :return:
        """
        if self.__body:
            return self.__body
        # generate fetch body RPC request data
        builder = runner_utils.new_builder()
        EIBody.Start(builder)
        body_req_data = EIBody.End(builder)
        val = self.__ask_extra_info(builder, EIInfo.Info.ReqBody, body_req_data)
        self.set_body(val)
        return val

    def set_body(self, body: str) -> bool:
        """
        set request body
        :param body:
        :return:
        """
        if body:
            self.__body = body
            return True
        return False

    def __ask_extra_info(self, builder: flatbuffers.Builder, ty, data) -> str:
        """
        nginx built-in variable and request body rpc calls
        :param builder:
        :param ty:
        :param data:
        :return:
        """
        res_val = []
        EIReq.Start(builder)
        EIReq.AddInfoType(builder, ty)
        EIReq.AddInfo(builder, data)
        res = EIReq.End(builder)
        builder.Finish(res)
        out = builder.Output()

        try:
            protocol = RunnerServerProtocol(out, runner_utils.RPC_EXTRA_INFO)
            protocol.encode()
            self.r.conn.sendall(protocol.buffer)
        except socket.timeout as e:
            self.r.log.info("connection timout: {}", e.args.__str__())
        except socket.error as e:
            self.r.log.error("connection error: {}", e.args.__str__())
        except BaseException as e:
            self.r.log.error("any error: {}", e.args.__str__())
        else:
            buf = self.r.conn.recv(runner_utils.RPC_PROTOCOL_HEADER_LEN)
            protocol = RunnerServerProtocol(buf, 0)
            err = protocol.decode()
            if err.code == RESP_STATUS_CODE_OK:
                buf = self.r.conn.recv(protocol.length)
                resp = EIResp.Resp.GetRootAs(buf)
                for i in range(resp.ResultLength()):
                    vector = resp.Result(i)
                    res_val.append(chr(vector))
            else:
                self.r.log.error(err.message)

        return "".join(res_val)

    def get_arg(self, key: str) -> str:
        """
        get request param
        :param key:
        :return:
        """
        return self.__args.get(key)

    def set_arg(self, key: str, value: str) -> bool:
        """
        set request param
        :param key:
        :param value:
        :return:
        """
        if key and value:
            self.__args[key] = value
            return True
        return False

    def get_args(self) -> dict:
        """
        get request params
        :return:
        """
        return self.__args

    def set_args(self, args: dict) -> bool:
        """
        set request params
        :param args:
        :return:
        """
        if args:
            self.__args = args
            return True
        return False

    def get_uri(self) -> str:
        """
        get request uri
        :return:
        """
        return self.__uri

    def set_uri(self, uri: str) -> bool:
        """
        set request uri
        :param uri:
        :return:
        """
        if uri and uri.startswith("/"):
            self.__uri = uri
            return True
        return False

    def get_remote_addr(self) -> str:
        """
        get request client ip address
        :return:
        """
        return self.__remote_addr

    def set_remote_addr(self, remote_addr: str) -> bool:
        """
        set request client ip address
        :param remote_addr:
        :return:
        """
        if remote_addr:
            self.__remote_addr = remote_addr
            return True
        return False

    def get_conf_token(self) -> int:
        """
        get request config token
        :return:
        """
        return self.__conf_token

    def set_conf_token(self, conf_token: int) -> bool:
        """
        set request config token
        :param conf_token:
        :return:
        """
        if conf_token:
            self.__conf_token = conf_token
            return True
        return False

    def get_id(self):
        """
        get request id
        :return:
        """
        return self.__id

    def set_id(self, id: int):
        """
        set request id
        :param id:
        :return:
        """
        if id:
            self.__id = id
            return True
        return False

    def set_method(self, method: str) -> bool:
        """
        set request method
        :param method:
        :return:
        """
        # support common request method setting
        if method and method.upper() in ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]:
            self.__method = method
            return True
        return False

    def get_method(self) -> str:
        """
        get request method
        :return:
        """
        return self.__method

    def set_config(self, key: str, value: str):
        """
        set plugin config
        :param key:
        :param value:
        :return:
        """
        if key:
            self.__configs[key] = value
            return True
        return False

    def get_config(self, key: str) -> str:
        """
        get plugin config
        :param key:
        :return:
        """
        return self.__configs.get(key)

    def get_configs(self) -> dict:
        """
        get plugin configs
        :return:
        """
        return self.__configs

    def set_configs(self, configs: dict) -> bool:
        """
        set plugin configs
        :return:
        """
        if configs:
            self.__configs = configs
            return True
        return False

    def __init(self) -> None:
        """
        init request handler
        :return:
        """
        if self.r.request.ty == runner_utils.RPC_HTTP_REQ_CALL:
            req = HCReq.Req.GetRootAsReq(self.r.request.data)

            # fetch request id
            self.set_id(req.Id())

            # fetch request conf token
            self.set_conf_token(req.ConfToken())

            # fetch request method
            self.set_method(runner_utils.get_method_name_by_code(req.Method()))

            # fetch request remote_addr
            ip_list = runner_utils.parse_list_vector(req, runner_utils.VECTOR_TYPE_SOURCE_IP, True)
            if len(ip_list) == 16:
                self.set_remote_addr(IPv6Address(bytes(ip_list)).exploded)
            else:
                self.set_remote_addr(IPv4Address(bytes(ip_list)).exploded)

            # fetch request uri
            self.set_uri(req.Path().decode())

            # fetch request headers
            hdr_dict = runner_utils.parse_dict_vector(req, runner_utils.VECTOR_TYPE_HEADER)
            self.set_headers(hdr_dict)

            # fetch request args
            arg_dict = runner_utils.parse_dict_vector(req, runner_utils.VECTOR_TYPE_QUERY)
            self.set_args(arg_dict)

        if self.r.request.ty == runner_utils.RPC_PREPARE_CONF:
            req = PCReq.Req.GetRootAsReq(self.r.request.data)
            for i in range(req.ConfLength()):
                # fetch request config
                name = req.Conf(i).Name().decode()
                config = req.Conf(i).Value().decode()
                self.set_config(name, config)

    def checked(self):
        """
        check request params is valid
        :return:
        """
        if len(self.__uri) == 0 and len(self.__headers) == 0 and len(self.__args) == 0:
            return False
        else:
            return True

    @runner_utils.response_config
    def config_handler(self, builder: flatbuffers.Builder):
        """
        get config setting response
        :param builder:
        :return:
        """
        return self.get_conf_token()

    @runner_utils.response_call(HCAction.Action.Rewrite)
    def call_handler(self, builder: flatbuffers.Builder):
        """
        get http call response
        :param builder:
        :return:
        """
        if not self.checked():
            return None, 0

        path_vector = runner_utils.create_str_vector(builder, self.get_uri())

        headers_vector = runner_utils.create_dict_vector(builder, self.get_headers(), HCAction.Action.Rewrite,
                                                         runner_utils.VECTOR_TYPE_HEADER)

        args_vector = runner_utils.create_dict_vector(builder, self.get_args(), HCAction.Action.Rewrite,
                                                      runner_utils.VECTOR_TYPE_QUERY)

        HCRw.RewriteStart(builder)
        HCRw.RewriteAddPath(builder, path_vector)
        HCRw.RewriteAddHeaders(builder, headers_vector)
        HCRw.RewriteAddArgs(builder, args_vector)
        rewrite = HCRw.RewriteEnd(builder)
        return rewrite, self.get_id()

    @runner_utils.response_unknown
    def unknown_handler(self, builder: flatbuffers.Builder):
        """
        get unknown response
        :param builder:
        :return:
        """
        return A6ErrCode.BAD_REQUEST
