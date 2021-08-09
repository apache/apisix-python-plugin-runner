from src.runner.socket.protocol import Protocol as NewServerProtocol
from src.runner.http.protocol import RPC_PREPARE_CONF
from src.runner.socket.response import RUNNER_SUCCESS_CODE
from src.runner.socket.response import RUNNER_SUCCESS_MESSAGE


def test_protocol_encode():
    buf_str = "Hello Python Runner".encode()
    protocol = NewServerProtocol(buffer=buf_str, ty=RPC_PREPARE_CONF)
    err = protocol.encode()
    buf_len = len(buf_str)
    buf_arr = bytearray(buf_len.to_bytes(4, byteorder="big"))
    buf_arr[0] = RPC_PREPARE_CONF
    buf_data = bytes(buf_arr) + buf_str
    buf_len = len(buf_data)
    assert err.code == RUNNER_SUCCESS_CODE
    assert err.message == RUNNER_SUCCESS_MESSAGE
    assert protocol.type == RPC_PREPARE_CONF
    assert protocol.buffer == buf_data
    assert protocol.length == buf_len


def test_protocol_decode():
    buf_str = "Hello Python Runner".encode()
    buf_len = len(buf_str)
    buf_arr = bytearray(buf_len.to_bytes(4, byteorder="big"))
    buf_arr[0] = RPC_PREPARE_CONF
    buf_data = bytes(buf_arr)
    protocol = NewServerProtocol(buffer=buf_data)
    err = protocol.decode()
    assert err.code == RUNNER_SUCCESS_CODE
    assert err.message == RUNNER_SUCCESS_MESSAGE
    assert protocol.type == RPC_PREPARE_CONF
    assert protocol.length == buf_len
