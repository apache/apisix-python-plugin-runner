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

import flatbuffers
from A6 import Method as A6Method
from A6 import TextEntry as A6Entry
from A6.Err.Code import Code as A6ErrCode
from A6.HTTPReqCall import Rewrite as HCRewrite
from A6.HTTPReqCall import Stop as HCStop
from A6.HTTPReqCall import Action as HCAction
from A6.HTTPReqCall import Resp as HCResp
from A6.PrepareConf import Resp as PCResp
from A6.Err import Resp as ErrResp

RPC_PROTOCOL_HEADER_LEN = 4

RPC_PREPARE_CONF = 1
RPC_HTTP_REQ_CALL = 2
RPC_EXTRA_INFO = 3
RPC_UNKNOWN = 0

VECTOR_TYPE_HEADER = 1
VECTOR_TYPE_QUERY = 2
VECTOR_TYPE_CONFIG = 3
VECTOR_TYPE_SOURCE_IP = 4

dictVectorParseFuncNames = {
    VECTOR_TYPE_HEADER: "Headers",
    VECTOR_TYPE_QUERY: "Args",
    VECTOR_TYPE_CONFIG: "Conf",
}

listVectorParseFuncNames = {
    VECTOR_TYPE_SOURCE_IP: "SrcIp",
}

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

methodNames = {
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

methodCodes = {
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


def create_dict_entry(builder: flatbuffers.Builder, data: dict) -> list:
    entries = []
    if not isinstance(data, dict) or len(data) <= 0:
        return entries
    for key in data:
        val = data[key]
        key_bytes = builder.CreateString(key)
        val_bytes = builder.CreateString(val)
        A6Entry.Start(builder)
        A6Entry.AddName(builder, key_bytes)
        A6Entry.AddValue(builder, val_bytes)
        entry = A6Entry.End(builder)
        entries.append(entry)
    return entries


def get_vector_object(action: int = 0, ty: int = 0):
    objects = {
        "%s:%s" % (HCAction.Action.Rewrite, VECTOR_TYPE_HEADER): HCRewrite.RewriteStartHeadersVector,
        "%s:%s" % (HCAction.Action.Rewrite, VECTOR_TYPE_QUERY): HCRewrite.RewriteStartArgsVector,
        "%s:%s" % (HCAction.Action.Stop, VECTOR_TYPE_HEADER): HCStop.StopStartHeadersVector,
    }
    return objects.get("%s:%s" % (action, ty), None)


def create_dict_vector(builder: flatbuffers.Builder, data: dict, action: int = 0, ty: int = 0):
    res = 0
    entries = create_dict_entry(builder, data)
    entries_len = len(entries)
    if entries_len == 0:
        return res

    vector_object = get_vector_object(action, ty)
    if not vector_object:
        return res

    vector_object(builder, entries_len)
    for i in range(entries_len - 1, -1, -1):
        builder.PrependUOffsetTRelative(entries[i])
    return builder.EndVector()


def create_str_vector(builder: flatbuffers.Builder, data: str):
    res = 0
    if not data or len(data) <= 0:
        return res

    data = data.encode(encoding="UTF-8")
    return builder.CreateByteVector(data)


def new_builder():
    return flatbuffers.Builder(256)


def get_method_name_by_code(code: int) -> str:
    return methodNames.get(code)


def get_method_code_by_name(name: str) -> int:
    return methodCodes.get(name)


def response_call(action_type: int):
    def decorator(func):
        def wrapper(cls, builder: flatbuffers.Builder):
            (action, id) = func(cls, builder)
            if not action or id == 0:
                return False

            HCResp.Start(builder)
            HCResp.AddId(builder, id)
            HCResp.AddActionType(builder, action_type)
            HCResp.AddAction(builder, action)
            res = HCResp.End(builder)
            builder.Finish(res)
            return True

        return wrapper

    return decorator


def response_config(func):
    def wrapper(cls, builder: flatbuffers.Builder):
        token = func(cls, builder)
        if token <= 0:
            return False

        PCResp.Start(builder)
        PCResp.AddConfToken(builder, token)
        res = PCResp.End(builder)
        builder.Finish(res)
        return True

    return wrapper


def response_unknown(func):
    def wrapper(cls, builder: flatbuffers.Builder):
        err_code = func(cls, builder)
        if not err_code:
            err_code = A6ErrCode.BAD_REQUEST
        ErrResp.Start(builder)
        ErrResp.AddCode(builder, err_code)
        res = ErrResp.End(builder)
        builder.Finish(res)
        return True

    return wrapper


def parse_dict_vector(cls: object, ty: int) -> dict:
    res = {}
    fn = dictVectorParseFuncNames.get(ty)
    if not fn:
        return res

    length = getattr(cls, "%sLength" % fn)()
    if not length or length == 0:
        return res

    for i in range(length):
        key = getattr(cls, fn)(i).Name().decode()
        val = getattr(cls, fn)(i).Value().decode()
        res[key] = val

    return res


def parse_list_vector(cls: object, ty: int, out_bytes: bool = False) -> list:
    res = []
    if out_bytes:
        res = bytearray()
    fn = listVectorParseFuncNames.get(ty)
    if not fn:
        return res

    length = getattr(cls, "%sLength" % fn)()
    if not length or length == 0:
        return res

    for i in range(length):
        val = getattr(cls, fn)(i)
        res.append(val)

    return res
