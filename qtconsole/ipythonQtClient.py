from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

# Script taken from:
# https://github.com/ipython/ipython/blob/7.16.x/examples/IPython%20Kernel/gui/gui-qt.py
# Transition from PyQt4 to PyQt5 in progress

"""
Simple Qt4 example to manually test event loop integration.
This is meant to run tests manually in ipython as:
In [5]: %gui qt
In [6]: %run gui-qt.py
Ref: Modified from http://zetcode.com/tutorials/pyqt4/firstprograms/
"""

class SimpleWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 200, 80)
        self.setWindowTitle('Hello World')

        quit = QPushButton('Close', self)
        quit.setGeometry(10, 10, 60, 35)

        # Old-style signals and slots (not implemented in PyQt5) -> to fix it,
        # see https://www.riverbankcomputing.com/static/Docs/PyQt4/new_style_signals_slots.html
        self.connect(quit, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('close()'))

if __name__ == '__main__':
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication([])

    sw = SimpleWindow()
    sw.show()

    try:
        from IPython.lib.guisupport import start_event_loop_qt4
        start_event_loop_qt4(app)
    except ImportError:
        app.exec_()

