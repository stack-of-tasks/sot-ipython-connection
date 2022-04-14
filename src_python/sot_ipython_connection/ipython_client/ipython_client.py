
import sys

import nest_asyncio
import jupyter_core

from PyQt5 import QtWidgets
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.client import QtKernelClient

nest_asyncio.apply()

class SOTClient(QtKernelClient):
    def __init__(self, kernel_number):
        self.load_connection_file(jupyter_core.paths.jupyter_runtime_dir() +
            '/kernel-' + kernel_number + '.json')
        self.start_channels()

    def run_python_command(self, cmd):
        self.execute(cmd, silent=False)

    def __del__(self):
        self.stop_channels()


def main(kernel_number, cmd1, cmd2):
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication(["test"])

    kernel_client = SOTClient(kernel_number)
    kernel_client.execute(cmd1, silent=False)
    kernel_client.execute(cmd2, silent=False)

if __name__ == "__main__":
    assert len(sys.argv) == 4
    main(sys.argv[1], sys.argv[2], sys.argv[3])