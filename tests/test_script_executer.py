import os
import sys
import unittest

from PyQt5 import QtWidgets

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from src_python.sot_ipython_connection.sot_client import SOTClient
from src_python.sot_ipython_connection.app.sot_script_executer import main as script_executer

class TestScriptExecuter(unittest.TestCase):
    """ These tests must be run after launching a new kernel
    """

    @classmethod
    def setUpClass(self):
        ...
        """ print(scriptDirectory + "/python_script_1.py")
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication([])

        self.kernel_client = SOTClient() """


    def test_var_definition(self):
        ...
        """ script_executer(scriptDirectory + "/python_script_1.py")
        self.kernel_client.run_python_command("script_var_1")
        self.kernel_client.run_python_command("script_var_2")

        assert len(self.kernel_client.cmd_history) == 2
        assert self.kernel_client.cmd_history[0].stdout == "1"
        assert self.kernel_client.cmd_history[0].stderr == None
        assert self.kernel_client.cmd_history[1].stdout == "2"
        assert self.kernel_client.cmd_history[1].stderr == None """
        

    def test_var_redefinition(self):
        ... # TODO


    def test_multiple_scripts_var_definition(self):
        ... # TODO


    def test_multiple_scripts_var_redefinition(self):
        ... # TODO
