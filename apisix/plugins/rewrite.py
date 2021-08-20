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

from apisix.runner.plugin.base import Base
from apisix.runner.http.request import Request
from apisix.runner.http.response import Response


class Rewrite(Base):
    def __init__(self):
        """
        Examples of `rewrite` type plugins, features:
            This type of plugin can customize the request `args`, `header`, and `path`
            This type of plugin does not interrupt the request
        """
        super(Rewrite, self).__init__(self.__class__.__name__)

    def filter(self, request: Request, response: Response):
        """
        The plugin executes the main function
        :param request:
            request parameters and information
        :param response:
            response parameters and information
        :return:
        """
        # Get plugin configuration information through `self.config`
        # print(self.config)

        # Rewrite request headers
        headers = request.headers
        headers["X-Resp-A6-Runner"] = "Python"
        response.headers = headers

        # Rewrite request args
        args = request.args
        args["a6_runner"] = "Python"
        response.args = args

        # Rewrite request path
        path = request.path
        response.path = path

        # Set plugin to `rewrite` type, default `rewrite`
        self.rewrite()
