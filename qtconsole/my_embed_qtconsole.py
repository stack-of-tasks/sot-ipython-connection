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

# The ID of an installed kernel, e.g. 'bash' or 'ir'.
USE_KERNEL = 'python3'

def make_jupyter_widget_with_kernel():
    """Start a kernel, connect to it, and create a RichJupyterWidget to use it
    """

    kernel_client = QtKernelClient()#connection_file=connection_file, config=self.config)
    kernel_client.load_connection_file('/home/jfricou/.local/share/jupyter/runtime/kernel-' +
        '66865' + '.json')
    kernel_client.start_channels()

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
