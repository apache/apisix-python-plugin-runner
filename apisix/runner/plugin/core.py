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
from typing import Any
from pkgutil import iter_modules
from apisix.runner.http.response import Response as HttpResponse
from apisix.runner.http.request import Request as HttpRequest

PLUGINS = {}


class PluginBase:

    def __init_subclass__(cls: Any, **kwargs):
        """
        register plugin object
        :param kwargs:
        :return:
        """
        name = cls.name(cls)
        if name not in PLUGINS:
            PLUGINS[name] = cls

    def name(self) -> str:
        """
        fetching plugin name
        :return:
        """
        pass

    def config(self, conf: Any) -> Any:
        """
        parsing plugin configuration
        :return:
        """
        pass

    def filter(self, conf: Any, req: HttpRequest, reps: HttpResponse) -> None:
        """
        execute plugin handler
        :param conf:  plugin configuration
        :param req:   request object
        :param reps:  response object
        :return:
        """
        pass


class PluginProcess:
    """
    plugin default package name
    """
    package = "apisix.plugins"

    @staticmethod
    def register():
        plugin_path = "%s/%s" % (os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                                 PluginProcess.package.replace(".", "/"))
        modules = iter_modules(path=[plugin_path])
        for _, mod_name, _ in modules:
            importlib.import_module("%s.%s" % (PluginProcess.package, mod_name))

    @staticmethod
    def execute(configs: dict, r, req: HttpRequest, reps: HttpResponse):
        for name, conf in configs.items():
            try:
                p = PLUGINS.get(name)()
                conf = p.config(conf)
                p.filter(conf, req, reps)
            except AttributeError as e:
                r.log.error("execute plugin `%s` AttributeError, %s" % (name, e.args.__str__()))
                return False
            except TypeError as e:
                r.log.error("execute plugin `%s` TypeError, %s" % (name, e.args.__str__()))
                return False
            except BaseException as e:
                r.log.error("execute plugin `%s` AnyError, %s" % (name, e.args.__str__()))
                return False
            else:
                if reps.changed():
                    break
        return True
