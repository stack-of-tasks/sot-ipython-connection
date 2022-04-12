"""An example of embedding a RichJupyterWidget in a PyQT Application.

This uses a normal kernel launched as a subprocess. It shows how to shutdown
the kernel cleanly when the application quits.

To run:

    python3 embed_qtconsole.py
"""
import sys
from PyQt5 import QtWidgets

from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.client import QtKernelClient
from jupyter_client import KernelClient
from jupyter_client.utils import run_sync
import nest_asyncio
import jupyter_core

""" Modified code from the qtconsole repo : qtconsoleapp.py (new_frontend_connection function)
and embed_qtconsole.py """

# The ID of an installed kernel, e.g. 'bash' or 'ir'.
USE_KERNEL = 'python3'

nest_asyncio.apply()

def make_jupyter_widget_with_kernel():
    """Start a kernel, connect to it, and create a RichJupyterWidget to use it
    """

    kernel_client = QtKernelClient()
    kernel_client.load_connection_file(jupyter_core.paths.jupyter_runtime_dir() +
        '/kernel-' + '19983' + '.json')
    kernel_client.start_channels()

    # TODO: make this work
    # execute_interactive = run_sync(KernelClient._async_execute_interactive)
    # execute_interactive(KernelClient, "b")

    # TODO: see what's in BaseFrontendMixin and QtKernelClientMixin (base_frontend_mixin.py)
    # TODO: try to use this code in myqtconsoleapp

    jupyter_widget = RichJupyterWidget()
    jupyter_widget.kernel_client = kernel_client
    return jupyter_widget

class MainWindow(QtWidgets.QMainWindow):
    """A window that contains a single Qt console."""
    def __init__(self):
        super().__init__()
        self.jupyter_widget = make_jupyter_widget_with_kernel()
        self.setCentralWidget(self.jupyter_widget)

    def shutdown_kernel(self):
        print('Shutting down kernel...')
        self.jupyter_widget.kernel_client.stop_channels()
        self.jupyter_widget.kernel_manager.shutdown_kernel()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(window.shutdown_kernel)
    sys.exit(app.exec_())
