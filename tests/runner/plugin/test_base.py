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

from apisix.runner.plugin.base import Base


def test_base():
    hello_name = "hello"
    hello_config = {"body": "apisix"}
    hello = Base(hello_name)
    hello.config = hello_config
    assert hello.name == hello_name
    assert hello.config == hello_config
    hello.name = "hello1"
    assert hello.name != hello_name

    world_name = "world"
    world_config = "apisxi"
    world = Base(world_name)
    world.config = world_config
    assert world.name == world_name
    assert world.config != world_config
    world.name = "world1"
    assert world.name != world_name
