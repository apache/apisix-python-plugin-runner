from src.runner.socket.error import Error as NewServerError
from src.runner.socket.error import RUNNER_ERROR_CODE
from src.runner.socket.error import RUNNER_SUCCESS_CODE
from src.runner.http.protocol import RPC_PREPARE_CONF
from src.runner.http.protocol import RPC_HTTP_REQ_CALL
from src.runner.http.protocol import RPC_UNKNOWN


def test_error_code():
    error = NewServerError(code=RUNNER_SUCCESS_CODE)
    assert error.code() == RUNNER_SUCCESS_CODE
    error = NewServerError(code=RUNNER_ERROR_CODE)
    assert error.code() == RUNNER_ERROR_CODE


def test_error_message():
    error = NewServerError(message="Hello Python Runner")
    assert error.message() == "Hello Python Runner"


def test_error_data():
    error = NewServerError(data="Hello Python Runner".encode())
    assert error.data() == b'Hello Python Runner'


def test_error_type():
    error = NewServerError(ty=RPC_UNKNOWN)
    assert error.type() == RPC_UNKNOWN
    error = NewServerError(ty=RPC_PREPARE_CONF)
    assert error.type() == RPC_PREPARE_CONF
    error = NewServerError(ty=RPC_HTTP_REQ_CALL)
    assert error.type() == RPC_HTTP_REQ_CALL
