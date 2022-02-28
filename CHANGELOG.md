---
title: Changelog
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

## Table of Contents

- [0.1.0](#010)
- [0.2.0](#020)

## 0.1.0

This release mainly provides basic features and adds test cases.

### Core

- complete project skeleton and available features.
- complete united test with [APISIX 2.7](https://github.com/apache/apisix/tree/release/2.7).
- supported debug mode.
- supported custom `stop` and `rewrite` plugin development.

[Back to TOC](#table-of-contents)

## 0.2.0

This release mainly refactors the operation objects of request/response and the way of automatic loading of plugins for
more efficient plugin development.

### Core

- `Request` and `Response` operation object refactoring.
- Plugin `auto registr` and `auto loading` refactoring.
- Supports getting the `request body` and `Nginx built-in variables` in the plugin.
- Specification and unifies the input and output of RPC requests.
- Inheritance interface for specification plugins.

[Back to TOC](#table-of-contents)
