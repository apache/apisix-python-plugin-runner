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
import apisix.runner.utils.common as runner_utils
from apisix.runner.utils.common import VECTOR_TYPE_HEADER
from apisix.runner.utils.common import VECTOR_TYPE_QUERY
from A6.HTTPReqCall import Rewrite as HCRewrite
from A6.HTTPReqCall import Stop as HCStop
from A6.HTTPReqCall import Action as HCAction


def test_get_method_code_by_name():
    for name in runner_utils.methodCodes:
        assert runner_utils.get_method_code_by_name(name) == runner_utils.methodCodes.get(name)


def test_get_method_name_by_code():
    for code in runner_utils.methodNames:
        assert runner_utils.get_method_name_by_code(code) == runner_utils.methodNames.get(code)


def test_new_builder():
    builder = runner_utils.new_builder()
    assert isinstance(builder, flatbuffers.Builder)
    assert builder.Bytes == flatbuffers.Builder(256).Bytes
    assert builder.Bytes != flatbuffers.Builder(512).Bytes


def test_create_dict_entry():
    builder = runner_utils.new_builder()
    entries = runner_utils.create_dict_entry(builder, {})
    assert not entries
    examples = {"q": "hello", "a": "world"}
    entries = runner_utils.create_dict_entry(builder, examples)
    assert len(entries) == 2


def test_create_dict_vector():
    builder = runner_utils.new_builder()
    b = runner_utils.create_dict_vector(builder, {})
    assert not b
    b = runner_utils.create_dict_vector(builder, {"q": "hello", "a": "world"}, HCAction.Action.Rewrite,
                                        VECTOR_TYPE_HEADER)
    assert b > 0
    b = runner_utils.create_dict_vector(builder, {"q": "hello", "a": "world"}, HCAction.Action.Rewrite,
                                        VECTOR_TYPE_QUERY)
    assert b > 0
    b = runner_utils.create_dict_vector(builder, {"q": "hello", "a": "world"}, HCAction.Action.Stop,
                                        VECTOR_TYPE_HEADER)
    assert b > 0
    b = runner_utils.create_dict_vector(builder, {"q": "hello", "a": "world"}, 0, 0)
    assert not b


def test_create_str_vector():
    builder = runner_utils.new_builder()
    b = runner_utils.create_str_vector(builder, "")
    assert not b
    b = runner_utils.create_str_vector(builder, "Hello")
    assert b


def test_get_vector_object():
    obj = runner_utils.get_vector_object(HCAction.Action.Rewrite, VECTOR_TYPE_HEADER)
    assert obj
    obj = runner_utils.get_vector_object(HCAction.Action.Rewrite, VECTOR_TYPE_QUERY)
    assert obj
    obj = runner_utils.get_vector_object(HCAction.Action.Stop, VECTOR_TYPE_HEADER)
    assert obj
    obj = runner_utils.get_vector_object(HCAction.Action.Stop, VECTOR_TYPE_QUERY)
    assert not obj
