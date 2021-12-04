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

import flatbuffers
import apisix.runner.plugin.core as runner_plugin
import apisix.runner.plugin.cache as runner_cache
import apisix.runner.utils.common as runner_utils
from apisix.runner.http.response import Response as NewHttpResponse
from apisix.runner.http.request import Request as NewHttpRequest
from A6.Err.Code import Code as ErrCode


class Handle:

    def __init__(self, r):
        """
        Init RPC Handle
        :param r:
            rpc request protocol type
        """
        self.r = r

    def dispatch(self) -> flatbuffers.Builder:
        # init builder
        builder = runner_utils.new_builder()
        # parse request
        req = NewHttpRequest(self.r)

        if self.r.request.ty == runner_utils.RPC_PREPARE_CONF:
            # generate token
            token = runner_cache.generate_token()
            # get plugins config
            configs = req.configs
            # cache plugins config
            ok = runner_cache.set_config_by_token(token, configs)
            if ok:
                req.conf_token = token
                ok = req.config_handler(builder)
                if not ok:
                    self.r.log.error("prepare conf request failure")
                    req.code = ErrCode.BAD_REQUEST
                    req.unknown_handler(builder)
            else:
                self.r.log.error("token `%d` cache setting failed" % token)
                req.code = ErrCode.CONF_TOKEN_NOT_FOUND
                req.unknown_handler(builder)

            return builder

        elif self.r.request.ty == runner_utils.RPC_HTTP_REQ_CALL:
            # get request token
            token = req.conf_token
            # get plugins
            configs = runner_cache.get_config_by_token(token)

            if len(configs) == 0:
                self.r.log.error("token `%d` cache acquisition failed" % token)
                req.code = ErrCode.CONF_TOKEN_NOT_FOUND
                req.unknown_handler(builder)
                return builder

            # init response
            resp = NewHttpResponse(self.r.request.ty)
            resp.id = req.id

            # execute plugins
            ok = runner_plugin.execute(configs, self.r, req, resp)
            if not ok:
                req.code = ErrCode.SERVICE_UNAVAILABLE
                req.unknown_handler(builder)
                return builder

            ok = resp.call_handler(builder)
            if ok:
                return builder

            ok = req.call_handler(builder)
            if not ok:
                self.r.log.error("http request call failure")
                req.code = ErrCode.BAD_REQUEST
                req.unknown_handler(builder)
                return builder

            return builder

        else:
            self.r.log.error("unknown request")
            req.code = ErrCode.BAD_REQUEST
            req.unknown_handler(builder)
            return builder
