import pytest
from PyQt5 import QtWidgets

from sot_ipython_connection.sot_client import SOTClient


@pytest.fixture(autouse=True)
def launch_kernel_and_app():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    yield


def test_namespace():
    kernel_client = SOTClient()

    kernel_client.run_python_command("initial_namespace_1")
    kernel_client.run_python_command("initial_namespace_2")
    kernel_client.run_python_command("initial_namespace_1 + initial_namespace_2")
    kernel_client.run_python_command("initial_namespace_3")

    assert len(kernel_client.cmd_history) == 4

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None
    assert kernel_client.cmd_history[2].stderr == None
    assert kernel_client.cmd_history[3].stderr != None

    assert kernel_client.cmd_history[0].stdout == "46"
    assert kernel_client.cmd_history[1].stdout == "54"
    assert kernel_client.cmd_history[2].stdout == "100"
    assert kernel_client.cmd_history[3].stdout == None