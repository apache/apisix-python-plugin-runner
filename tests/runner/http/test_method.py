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

import apisix.runner.http.method as RunnerMethod
from a6pluginproto import Method as A6Method


def test_get_name_by_code():
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodGET) == A6Method.Method.GET
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodHEAD) == A6Method.Method.HEAD
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodPOST) == A6Method.Method.POST
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodPUT) == A6Method.Method.PUT
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodDELETE) == A6Method.Method.DELETE
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodMKCOL) == A6Method.Method.MKCOL
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodCOPY) == A6Method.Method.COPY
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodMOVE) == A6Method.Method.MOVE
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodOPTIONS) == A6Method.Method.OPTIONS
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodPROPFIND) == A6Method.Method.PROPFIND
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodPROPPATCH) == A6Method.Method.PROPPATCH
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodLOCK) == A6Method.Method.LOCK
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodUNLOCK) == A6Method.Method.UNLOCK
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodPATCH) == A6Method.Method.PATCH
    assert RunnerMethod.get_code_by_name(RunnerMethod.A6MethodTRACE) == A6Method.Method.TRACE


def test_get_code_by_name():
    assert RunnerMethod.get_name_by_code(A6Method.Method.GET) == RunnerMethod.A6MethodGET
    assert RunnerMethod.get_name_by_code(A6Method.Method.HEAD) == RunnerMethod.A6MethodHEAD
    assert RunnerMethod.get_name_by_code(A6Method.Method.POST) == RunnerMethod.A6MethodPOST
    assert RunnerMethod.get_name_by_code(A6Method.Method.PUT) == RunnerMethod.A6MethodPUT
    assert RunnerMethod.get_name_by_code(A6Method.Method.DELETE) == RunnerMethod.A6MethodDELETE
    assert RunnerMethod.get_name_by_code(A6Method.Method.MKCOL) == RunnerMethod.A6MethodMKCOL
    assert RunnerMethod.get_name_by_code(A6Method.Method.COPY) == RunnerMethod.A6MethodCOPY
    assert RunnerMethod.get_name_by_code(A6Method.Method.MOVE) == RunnerMethod.A6MethodMOVE
    assert RunnerMethod.get_name_by_code(A6Method.Method.OPTIONS) == RunnerMethod.A6MethodOPTIONS
    assert RunnerMethod.get_name_by_code(A6Method.Method.PROPFIND) == RunnerMethod.A6MethodPROPFIND
    assert RunnerMethod.get_name_by_code(A6Method.Method.PROPPATCH) == RunnerMethod.A6MethodPROPPATCH
    assert RunnerMethod.get_name_by_code(A6Method.Method.LOCK) == RunnerMethod.A6MethodLOCK
    assert RunnerMethod.get_name_by_code(A6Method.Method.UNLOCK) == RunnerMethod.A6MethodUNLOCK
    assert RunnerMethod.get_name_by_code(A6Method.Method.PATCH) == RunnerMethod.A6MethodPATCH
    assert RunnerMethod.get_name_by_code(A6Method.Method.TRACE) == RunnerMethod.A6MethodTRACE
