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
import click

from apisix.runner.server.server import Server as NewServer
from apisix.runner.server.config import Config as NewConfig

RUNNER_VERSION = "0.1.0"


@click.group()
@click.version_option(version=RUNNER_VERSION)
def runner() -> None:
    pass


@runner.command()
def start() -> None:
    config = NewConfig(os.path.dirname(os.path.abspath(__file__)))
    server = NewServer(config)
    server.receive()


def main() -> None:
    runner()


if __name__ == '__main__':
    main()
