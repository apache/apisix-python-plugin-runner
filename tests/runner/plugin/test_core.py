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
from pkgutil import iter_modules
from apisix.runner.plugin.core import loading as plugin_loading
from apisix.runner.plugin.core import execute as plugin_execute
from apisix.runner.http.request import Request as NewHttpRequest
from apisix.runner.http.response import Response as NewHttpResponse
from apisix.runner.server.response import RESP_STATUS_CODE_OK
from apisix.runner.server.response import RESP_STATUS_CODE_SERVICE_UNAVAILABLE
from apisix.runner.server.response import RESP_STATUS_CODE_BAD_REQUEST


class Test:
    """
    test plugin
    """
    def filter(self):
        """
        test plugin handler
        :return:
        """
        pass


def test_loading():
    configs = plugin_loading()
    assert isinstance(configs, dict)
    config_keys = configs.keys()
    path = "%s/plugins" % os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    modules = iter_modules(path=[path])
    for _, name, _ in modules:
        assert name in config_keys


def test_execute():
    request = NewHttpRequest()
    response = NewHttpResponse()
    configs = plugin_loading()
    for p_name in configs:
        configs[p_name] = configs.get(p_name)()
    (code, _) = plugin_execute(configs, request, response)
    assert code == RESP_STATUS_CODE_OK
    (code, _) = plugin_execute(configs, request, None)
    assert code == RESP_STATUS_CODE_SERVICE_UNAVAILABLE
    configs["test"] = Test()
    (code, _) = plugin_execute(configs, request, response)
    assert code == RESP_STATUS_CODE_BAD_REQUEST
