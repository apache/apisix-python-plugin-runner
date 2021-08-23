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
import yaml
import logging


class _ConfigSocket:

    def __init__(self):
        """
        init socket config handler
        """
        self.file = "/tmp/runner.sock"

    @property
    def file(self):
        """
        get config file for socket
        :return:
        """
        return self._file

    @file.setter
    def file(self, file: str) -> None:
        """
        set config file for socket
        :param file:
        :return:
        """
        self._file = file.replace("unix:", "")


class _ConfigLogging:

    def __init__(self):
        self.level = "NOTSET"

    @property
    def level(self) -> int:
        """
        get config level for socket
        :return:
        """
        return self._level

    @level.setter
    def level(self, level: str) -> None:
        """
        set config level for socket
        :param level:
        :return:
        """
        level = level.upper()
        _name_to_level = {
            'ERROR': logging.ERROR,
            'WARN': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'NOTSET': logging.NOTSET,
        }
        self._level = _name_to_level.get(level, logging.NOTSET)


class Config:

    def __init__(self, config_path: str = "", config_name: str = "config.yaml"):
        """
        init config
        :param config_path:
            local config file path
        :param config_name:
            local config file name
        """
        self.socket = _ConfigSocket()
        self.logging = _ConfigLogging()
        self._loading_config(config_path, config_name)

    @staticmethod
    def _get_env_config(config: str):
        """
        get the configuration in the local environment variable
        :param config:
        :return:
        """
        if isinstance(config, str) and config.find("$env.") != -1:
            env_name = config.replace("$env.", "")
            return os.getenv(env_name)
        return config

    def _loading_config(self, config_path: str, config_name: str):
        """
        load local configuration file
        :param config_path:
        :param config_name:
        :return:
        """
        if len(config_path) and os.path.exists(config_path):
            abs_path = config_path
        else:
            abs_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        cf_path = "%s/%s" % (abs_path, config_name)
        if not os.path.exists(cf_path):
            print("ERR: config file `%s` not exists" % cf_path)
            exit(1)

        # reading config file
        fs = open(cf_path, encoding="UTF-8")
        configs = yaml.load(fs, Loader=yaml.FullLoader)

        # socket config
        socket = configs.get("socket", {})
        socket_file = self._get_env_config(socket.get("file"))
        if socket_file:
            self.socket.file = socket_file

        # logging config
        logger = configs.get("logging", {})
        logger_level = self._get_env_config(logger.get("level"))
        if logger_level:
            self.logging.level = logger_level
