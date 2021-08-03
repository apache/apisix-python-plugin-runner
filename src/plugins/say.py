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
import runner.plugin.base
from runner.http.request import Request
from runner.http.response import Response


class Say(runner.plugin.base.Base):
    def __init__(self):
        super(Say, self).__init__(self.__class__.__name__)

    def filter(self, request: Request, response: Response):
        response.setHeader("X-Resp-A6-Runner", "Python")
        response.setBody("Hello, Python Runner of APISIX")
