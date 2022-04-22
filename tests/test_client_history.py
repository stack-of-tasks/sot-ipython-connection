import pytest
from PyQt5 import QtWidgets

from src_python.sot_ipython_connection.sot_client import SOTClient


# TODO: update the stderr tests (now using SOTCommandError)

@pytest.fixture(autouse=True)
def launch_kernel_and_app():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    yield
       

def test_no_cmd():
    kernel_client = SOTClient()
    assert len(kernel_client.cmd_history) == 0


def test_one_cmd_successful():
    kernel_client = SOTClient()
    kernel_client.run_python_command("1 + 1")

    assert len(kernel_client.cmd_history) == 1

    assert kernel_client.cmd_history[0].session_id != None
    assert kernel_client.cmd_history[0].id != None
    assert kernel_client.cmd_history[0].content == "1 + 1"
    assert kernel_client.cmd_history[0].stdout == "2"
    assert kernel_client.cmd_history[0].stderr == None


def test_one_cmd_error():
    kernel_client = SOTClient()
    kernel_client.run_python_command("unknown_variable")

    assert len(kernel_client.cmd_history) == 1

    assert kernel_client.cmd_history[0].session_id != None
    assert kernel_client.cmd_history[0].id != None
    assert kernel_client.cmd_history[0].content == "unknown_variable"
    assert kernel_client.cmd_history[0].stdout == None
    assert kernel_client.cmd_history[0].stderr != None
    

def test_several_cmd():
    kernel_client = SOTClient()
    kernel_client.run_python_command("test_history_1 = 1")
    kernel_client.run_python_command("test_history_1")

    assert len(kernel_client.cmd_history) == 2

    assert kernel_client.cmd_history[0].session_id == kernel_client.session_id
    assert kernel_client.cmd_history[0].id != None
    assert kernel_client.cmd_history[0].content == "test_history_1 = 1"
    assert kernel_client.cmd_history[0].stdout == None
    assert kernel_client.cmd_history[0].stderr == None

    assert kernel_client.cmd_history[1].session_id == kernel_client.session_id
    assert kernel_client.cmd_history[1].id != None
    assert kernel_client.cmd_history[1].content == "test_history_1"
    assert kernel_client.cmd_history[1].stdout == "1"
    assert kernel_client.cmd_history[1].stderr == None

    assert kernel_client.cmd_history[1].id != kernel_client.cmd_history[0].id
    

def test_several_sessions():
    ... # TODO
    

def test_self_history():
    ... # TODO: compare history and self history after several clients have sent commands
