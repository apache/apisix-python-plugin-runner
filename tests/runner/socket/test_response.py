from src.runner.socket.response import Response as NewServerResponse
from src.runner.socket.response import RUNNER_ERROR_CODE
from src.runner.socket.response import RUNNER_SUCCESS_CODE
from src.runner.http.protocol import RPC_PREPARE_CONF
from src.runner.http.protocol import RPC_HTTP_REQ_CALL
from src.runner.http.protocol import RPC_UNKNOWN


def test_response_code():
    response = NewServerResponse(code=RUNNER_SUCCESS_CODE)
    assert response.code == RUNNER_SUCCESS_CODE
    error = NewServerResponse(code=RUNNER_ERROR_CODE)
    assert error.code == RUNNER_ERROR_CODE


def test_response_message():
    response = NewServerResponse(message="Hello Python Runner")
    assert response.message == "Hello Python Runner"


def test_response_data():
    response = NewServerResponse(data="Hello Python Runner".encode())
    assert response.data == b'Hello Python Runner'


def test_response_type():
    response = NewServerResponse(ty=RPC_UNKNOWN)
    assert response.type == RPC_UNKNOWN
    response = NewServerResponse(ty=RPC_PREPARE_CONF)
    assert response.type == RPC_PREPARE_CONF
    response = NewServerResponse(ty=RPC_HTTP_REQ_CALL)
    assert response.type == RPC_HTTP_REQ_CALL


def test_response_eq():
    resp1 = NewServerResponse(code=RUNNER_SUCCESS_CODE, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    resp2 = NewServerResponse(code=RUNNER_ERROR_CODE, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    resp3 = NewServerResponse(code=RUNNER_SUCCESS_CODE, message="Hello Python Runner",
                              data="Hello Python Runner".encode(), ty=RPC_PREPARE_CONF)
    assert resp1 != resp2
    assert resp1 == resp3
