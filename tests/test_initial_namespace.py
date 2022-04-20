import os
import sys

from PyQt5 import QtWidgets

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from src_python.sot_ipython_connection.sot_client import SOTClient

class TestInitialNamespace:
    """ These tests must be run after launching a new kernel
    """
    
    @classmethod
    def setUpClass(self):
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication([])
        app.setQuitOnLastWindowClosed(False)


    def test_namespace(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("initial_namespace_1")
        kernel_client.run_python_command("initial_namespace_2")
        kernel_client.run_python_command("initial_namespace_1 + initial_namespace_2")
        kernel_client.run_python_command("initial_namespace_3")

        assert len(kernel_client.cmd_history) == 4

        assert kernel_client.cmd_history[0].stdout == "46"
        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stdout == "54"
        assert kernel_client.cmd_history[1].stderr == None
        assert kernel_client.cmd_history[2].stdout == "100"
        assert kernel_client.cmd_history[2].stderr == None
        assert kernel_client.cmd_history[3].stdout == None