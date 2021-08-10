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
from a6pluginproto import Method as A6Method

A6MethodGET = "GET"
A6MethodHEAD = "HEAD"
A6MethodPOST = "POST"
A6MethodPUT = "PUT"
A6MethodDELETE = "DELETE"
A6MethodMKCOL = "MKCOL"
A6MethodCOPY = "COPY"
A6MethodMOVE = "MOVE"
A6MethodOPTIONS = "OPTIONS"
A6MethodPROPFIND = "PROPFIND"
A6MethodPROPPATCH = "PROPPATCH"
A6MethodLOCK = "LOCK"
A6MethodUNLOCK = "UNLOCK"
A6MethodPATCH = "PATCH"
A6MethodTRACE = "TRACE"

methodName = {
    A6Method.Method.GET: A6MethodGET,
    A6Method.Method.HEAD: A6MethodHEAD,
    A6Method.Method.POST: A6MethodPOST,
    A6Method.Method.PUT: A6MethodPUT,
    A6Method.Method.DELETE: A6MethodDELETE,
    A6Method.Method.MKCOL: A6MethodMKCOL,
    A6Method.Method.COPY: A6MethodCOPY,
    A6Method.Method.MOVE: A6MethodMOVE,
    A6Method.Method.OPTIONS: A6MethodOPTIONS,
    A6Method.Method.PROPFIND: A6MethodPROPFIND,
    A6Method.Method.PROPPATCH: A6MethodPROPPATCH,
    A6Method.Method.LOCK: A6MethodLOCK,
    A6Method.Method.UNLOCK: A6MethodUNLOCK,
    A6Method.Method.PATCH: A6MethodPATCH,
    A6Method.Method.TRACE: A6MethodTRACE,
}

methodCode = {
    A6MethodGET: A6Method.Method.GET,
    A6MethodHEAD: A6Method.Method.HEAD,
    A6MethodPOST: A6Method.Method.POST,
    A6MethodPUT: A6Method.Method.PUT,
    A6MethodDELETE: A6Method.Method.DELETE,
    A6MethodMKCOL: A6Method.Method.MKCOL,
    A6MethodCOPY: A6Method.Method.COPY,
    A6MethodMOVE: A6Method.Method.MOVE,
    A6MethodOPTIONS: A6Method.Method.OPTIONS,
    A6MethodPROPFIND: A6Method.Method.PROPFIND,
    A6MethodPROPPATCH: A6Method.Method.PROPPATCH,
    A6MethodLOCK: A6Method.Method.LOCK,
    A6MethodUNLOCK: A6Method.Method.UNLOCK,
    A6MethodPATCH: A6Method.Method.PATCH,
    A6MethodTRACE: A6Method.Method.TRACE,
}


def get_name_by_code(code: int) -> str:
    return methodName.get(code)


def get_code_by_name(name: str) -> int:
    return methodCode.get(name)
