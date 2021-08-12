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
from minicache import cache

RUNNER_CACHE_TOKEN = "RUNNER:CACHE:TOKEN"
RUNNER_CACHE_ENTRY = "RUNNER:CACHE:ENTRY"


def generate_token() -> int:
    token = cache.get(RUNNER_CACHE_TOKEN, 0)
    token = token + 1
    cache.update(RUNNER_CACHE_TOKEN, token)
    return token


def set_config_by_token(token: int, configs: dict) -> bool:
    cache_key = "%s:%s" % (RUNNER_CACHE_ENTRY, token)
    cache.update(cache_key, configs)
    return cache.has(cache_key)


def get_config_by_token(token: int):
    cache_key = "%s:%s" % (RUNNER_CACHE_ENTRY, token)
    return cache.get(cache_key, {})
