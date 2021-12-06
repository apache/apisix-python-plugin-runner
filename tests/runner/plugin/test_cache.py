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

from apisix.runner.plugin.cache import generate_token
from apisix.runner.plugin.cache import get_config_by_token
from apisix.runner.plugin.cache import set_config_by_token


def test_cache():
    cache_config = {"hello": "world"}
    token = generate_token()
    config = get_config_by_token(token)
    assert not config
    ok = set_config_by_token(token, cache_config)
    assert ok
    config = get_config_by_token(token)
    assert config == cache_config


def test_generate_token():
    token = generate_token()
    assert token


def test_set_config_by_token():
    ok = set_config_by_token(1, {})
    assert not ok
    ok = set_config_by_token(1, {"q": "hello"})
    assert ok


def test_get_config_by_token():
    token = 1
    data = {"q": "hello"}
    ok = set_config_by_token(token, data)
    assert ok
    d = get_config_by_token(token)
    assert d == data
