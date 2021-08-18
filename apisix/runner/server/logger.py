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

import sys
import logging


class Logger:
    def __init__(self, level: int = logging.NOTSET):
        """
        init server logger handler
        :param level:
            logger level
        """
        self.logger = logging
        self._init(level)

    def set_level(self, level: int):
        """
        set level and reset logger
        :param level:
        :return:
        """
        self._init(level)

    def _init(self, level: int):
        """
        init logger
        :param level:
        :return:
        """
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message: str, *objs):
        """
        info level logger output
        :param message:
        :param objs:
        :return:
        """
        self.logger.info(message.format(*objs))

    def error(self, message: str, *objs):
        """
        error level logger output
        :param message:
        :param objs:
        :return:
        """
        self.logger.error(message.format(*objs))

    def debug(self, message: str, *objs):
        """
        debug level logger output
        :param message:
        :param objs:
        :return:
        """
        self.logger.debug(message.format(*objs))

    def warn(self, message: str, *objs):
        """
        warning level logger output
        :param message:
        :param objs:
        :return:
        """
        self.logger.warning(message.format(*objs))
