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

from typing import Any
from apisix.runner.http.request import Request
from apisix.runner.http.response import Response
from apisix.runner.plugin.core import PluginBase


class Stop(PluginBase):

    def name(self) -> str:
        """
        The name of the plugin registered in the runner
        :return:
        """
        return "stop"

    def config(self, conf: Any) -> Any:
        """
        Parse plugin configuration
        :param conf:
        :return:
        """
        return conf

    def filter(self, conf: Any, request: Request, response: Response):
        """
        The plugin executes the main function
        :param conf:
            plugin configuration after parsing
        :param request:
            request parameters and information
        :param response:
            response parameters and information
        :return:
        """

        # print plugin configuration
        print(conf)

        # Fetch request nginx variable `host`
        host = request.get_var("host")
        print(host)

        # Fetch request body
        body = request.get_body()
        print(body)

        # Set response headers
        response.set_header("X-Resp-A6-Runner", "Python")

        # Set response body
        response.set_body("Hello, Python Runner of APISIX")

        # Set response status code
        response.set_status_code(201)
