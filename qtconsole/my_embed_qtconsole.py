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


nest_asyncio.apply()

# The ID of an installed kernel, e.g. 'bash' or 'ir'.
USE_KERNEL = 'python3'

def make_jupyter_widget_with_kernel():
    """Start a kernel, connect to it, and create a RichJupyterWidget to use it
    """

    # Using code in qtconsoleapp.py (new_frontend_connection function) and in
    # embed_qtconsole.py
    kernel_client = QtKernelClient()#connection_file=connection_file, config=self.config)
    kernel_client.load_connection_file('/home/jfricou/.local/share/jupyter/runtime/kernel-' +
        '32675' + '.json') # Opens the given connection file and stores it
    kernel_client.start_channels()

    # TODO: make this work
    # execute_interactive = run_sync(KernelClient._async_execute_interactive)
    # execute_interactive(KernelClient, "b")

    # TODO: see what's in BaseFrontendMixin (base_frontend_mixin.py)

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
