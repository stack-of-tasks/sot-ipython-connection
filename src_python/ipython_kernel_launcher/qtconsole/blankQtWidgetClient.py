import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    window.show()
    app.exec_()

    # Network programming with PyQt:
    # https://doc.qt.io/qtforpython/overviews/qtnetwork-programming.html