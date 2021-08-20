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
import importlib
from pkgutil import iter_modules
from typing import Tuple
from apisix.runner.server.response import RESP_STATUS_CODE_OK
from apisix.runner.server.response import RESP_STATUS_MESSAGE_OK
from apisix.runner.server.response import RESP_STATUS_CODE_SERVICE_UNAVAILABLE
from apisix.runner.server.response import RESP_STATUS_CODE_BAD_REQUEST


def execute(configs: dict, request, response) -> Tuple[int, str]:
    for name in configs:
        plugin = configs.get(name)
        if type(plugin).__name__.lower() != name.lower():
            return RESP_STATUS_CODE_BAD_REQUEST, "execute plugin `%s`, plugin handler is not object" % name

        try:
            plugin.filter(request, response)
        except AttributeError as e:
            return RESP_STATUS_CODE_SERVICE_UNAVAILABLE, "execute plugin `%s`, %s" % (name, e.args.__str__())
        except TypeError as e:
            return RESP_STATUS_CODE_BAD_REQUEST, "execute plugin `%s`, %s" % (name, e.args.__str__())
        else:
            response.action_type = plugin.action

    return RESP_STATUS_CODE_OK, RESP_STATUS_MESSAGE_OK


def loading() -> dict:
    path = "%s/plugins" % os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    modules = iter_modules(path=[path])
    plugins = {}

    for loader, moduleName, _ in modules:
        classNameConversion = list(map(lambda name: name.capitalize(), moduleName.split("_")))
        className = "".join(classNameConversion)
        classInstance = getattr(importlib.import_module("apisix.plugins.%s" % moduleName), className)
        plugins[str(moduleName).lower()] = classInstance

    return plugins
