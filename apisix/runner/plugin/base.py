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

from apisix.runner.http.response import PLUGIN_ACTION_REWRITE
from apisix.runner.http.response import PLUGIN_ACTION_STOP


class Base:
    def __init__(self, name: str):
        """
        plugin base class
        :param name:
            instance plugin name
        """
        self._name = name
        self._config = {}
        self._action = PLUGIN_ACTION_REWRITE

    @property
    def name(self) -> str:
        """
        get plugin type
        :return:
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        set plugin type
        :param name:
        :return:
        """
        self._name = name

    @property
    def config(self) -> dict:
        """
        set plugin config
        :return:
        """
        return self._config

    @config.setter
    def config(self, config: dict) -> None:
        """
        get plugin config
        :param config:
        :return:
        """
        if config and isinstance(config, dict):
            self._config = config
        else:
            self._config = {}

    @property
    def action(self) -> int:
        """
        get plugin type
        :return:
        """
        return self._action

    @action.setter
    def action(self, action: int) -> None:
        """
        set plugin type
        :param action:
        :return:
        """
        self._action = action

    def stop(self) -> None:
        """
        Set plugin to `Stop` type
        :return:
        """
        self.action = PLUGIN_ACTION_STOP

    def rewrite(self) -> None:
        """
        Set plugin to `Rewrite` type
        :return:
        """
        self.action = PLUGIN_ACTION_REWRITE
