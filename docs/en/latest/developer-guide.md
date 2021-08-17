---
title: Developer Guide
---

<!--
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
-->

## Overview

This documentation explains how to develop this project.


## Prerequisites

* Python 3.6+
* APISIX 2.7.0


## Debug

- Run `make setup` Installation dependencies
- Run `export PYTHONPATH=$PYTHONPATH:/path/to/apisix-python-plugin-runner` loading project path 
- Run `APISIX_LISTEN_ADDRESS=unix:/tmp/runner.sock python3 apisix/main.py start`
to start it.


## Plugin

#### Plugin directory
```
/path/to/apisix-python-plugin-runner/apisix/plugin
```
the `.py` files in this directory autoload


#### Plugin example
```
/path/to/apisix-python-plugin-runner/apisix/plugin/say.py
```

#### Plugin Format
```python
from apisix.runner.plugin.base import Base
from apisix.runner.http.request import Request
from apisix.runner.http.response import Response


class Say(Base):
    def __init__(self):
        super(Say, self).__init__(self.__class__.__name__)

    def filter(self, request: Request, response: Response):
        headers = request.headers
        headers["X-Resp-A6-Runner"] = "Python"
        response.body = "Hello, Python Runner of APISIX"
        response.headers = headers
```
- The plugin must inherit the `Base` class
- The plugin must implement the `filter` function
- `filter` function parameters can only contain `Request` and `Response` classes as parameters
- Request parameter can get request information
- Response parameter can set response information
- `self.config` can get plug-in configuration information


## Test

Run `make test`.


## Data Format

[FlatBuffers](https://github.com/google/flatbuffers)


## Data Protocol

```
1 byte of type + 3 bytes of length + data
```