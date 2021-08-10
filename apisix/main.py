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
import sys
import click

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from apisix.runner.plugin.core import loading

RUNNER_VERSION = "0.1.0"
RUNNER_SOCKET = "/tmp/runner.sock"


@click.group()
@click.version_option(version=RUNNER_VERSION)
def runner() -> None:
    pass


@runner.command()
@click.option('--debug/--no-debug', help='enable or disable debug, default disable.', default=False)
def start(debug) -> None:
    click.echo(debug)
    loading()
    # server = NewServer(RUNNER_SOCKET)
    # server.receive()


def main() -> None:
    runner()


if __name__ == '__main__':
    main()
