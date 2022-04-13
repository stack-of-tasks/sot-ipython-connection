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
    if len(sys.argv) == 1:
        exit()
    kernel_client.load_connection_file(jupyter_core.paths.jupyter_runtime_dir() +
        '/kernel-' + sys.argv[1] + '.json')
    kernel_client.start_channels()

    jupyter_widget = RichJupyterWidget() # TODO: see how it handles input / output
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
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication([])

    # TODO: replace MainWindow with a custom class inheriting from
    # QWidget: https://www.riverbankcomputing.com/static/Docs/PyQt4/qwidget.html
    # https://courspython.com/interfaces-pyqt4.html
    window = MainWindow()
    window.show()

    app.aboutToQuit.connect(window.shutdown_kernel)

    # TODO:
    """ QtWidgets.QApplication.sendEvent(self._text_edit, event) """

    # TODO:
    # see if _append_plain_text is called when data is received from the
    # kernel: _event_filter_console_keypress in console_widget.py
    if len(sys.argv) > 2:
        window.jupyter_widget.kernel_client.execute(sys.argv[2], silent=False)

    sys.exit(app.exec_()) # Main loop
