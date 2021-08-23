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
import logging
from apisix.runner.server.config import Config as NewServerConfig


def test_config_default():
    config = NewServerConfig()

    config.logging.level = "INFO"
    assert config.logging.level == logging.INFO

    config.logging.level = "ERROR"
    assert config.logging.level == logging.ERROR

    config.logging.level = "WARN"
    assert config.logging.level == logging.WARNING

    config.logging.level = "NOTSET"
    assert config.logging.level == logging.NOTSET

    config.socket.file = "/test/runner.sock"
    assert config.socket.file == "/test/runner.sock"


def test_config_custom():
    config = NewServerConfig("%s/apisix" % os.path.abspath(os.path.join(os.getcwd())), "config.yaml")

    config.logging.level = "NOTSET"
    assert config.logging.level == logging.NOTSET

    config.logging.level = "INFO"
    assert config.logging.level == logging.INFO

    config.logging.level = "ERROR"
    assert config.logging.level == logging.ERROR

    config.logging.level = "WARN"
    assert config.logging.level == logging.WARNING

    config.socket.file = "/test/runner.sock"
    assert config.socket.file == "/test/runner.sock"
