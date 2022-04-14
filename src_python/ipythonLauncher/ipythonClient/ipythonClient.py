
import sys

import nest_asyncio
import jupyter_core

from PyQt5 import QtWidgets
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.client import QtKernelClient

nest_asyncio.apply()

def shutdown_kernel():
    ...

class SOTClient(QtKernelClient):
    def __init__(self, kernel_number):
        self.load_connection_file(jupyter_core.paths.jupyter_runtime_dir() +
            '/kernel-' + kernel_number + '.json')
        self.start_channels()

    def run_python_command(self, cmd):
        self.execute(cmd, silent=False)

    """ def __del__(self):
        self.stop_channels() """


def main(kernel_number, cmd):
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication(["test"])

    kernel_client = SOTClient(kernel_number)

    jupyter_widget = RichJupyterWidget()
    jupyter_widget.kernel_client = kernel_client

    app.aboutToQuit.connect(shutdown_kernel)
    kernel_client.execute(cmd, silent=False)
    jupyter_widget.kernel_manager.shutdown_kernel()

    sys.exit(app.exec_())

if __name__ == "__main__":
    assert len(sys.argv) == 3
    main(sys.argv[1], sys.argv[2])