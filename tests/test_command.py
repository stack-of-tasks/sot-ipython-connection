import os
import sys

from PyQt5 import QtWidgets

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from src_python.sot_ipython_connection.sot_client import SOTClient

class TestCommand:
    """ These tests must be run after launching a new kernel
    """
    
    @classmethod
    def setUpClass(self):
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication([])
        app.setQuitOnLastWindowClosed(False)
        

    def test_var_definition(self):
        ... # TODO


    def test_var_redefinition(self):
        ... # TODO


    def test_operations(self):
        ... # TODO
        

    def test_undefined_var(self):
        ... # TODO
        

    def test_import(self):
        ... # TODO
