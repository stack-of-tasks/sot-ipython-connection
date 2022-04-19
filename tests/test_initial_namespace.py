import os
import sys

from PyQt5 import QtWidgets

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from src_python.sot_ipython_connection.app.sot_interpreter import main as launch_kernel
from src_python.sot_ipython_connection.sot_client import SOTClient

class TestInitialNamespace:
    """ These tests must be run after launching a kernel
    """

    def test_namespace(self):
        app = QtWidgets.QApplication.instance() 
        if not app:
            app = QtWidgets.QApplication([])

        kernel_client = SOTClient()
        kernel_client.run_python_command("a")
        kernel_client.run_python_command("b")
        kernel_client.run_python_command("a + b")
        kernel_client.run_python_command("c")

        assert len(kernel_client.cmd_history) == 4

        assert kernel_client.cmd_history[0].stdout == "46"
        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stdout == "54"
        assert kernel_client.cmd_history[1].stderr == None
        assert kernel_client.cmd_history[2].stdout == "100"
        assert kernel_client.cmd_history[2].stderr == None
        assert kernel_client.cmd_history[3].stdout == None