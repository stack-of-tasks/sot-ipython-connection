import sys
import os

from PyQt5 import QtWidgets

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from sot_client import SOTClient

def main():
    # TODO: launch the qt client
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication([])

    kernel_client = SOTClient()
    kernel_client.run_python_command("op = 4")


if __name__ == "__main__":
    main()