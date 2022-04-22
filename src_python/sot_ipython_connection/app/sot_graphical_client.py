from PyQt5 import QtWidgets

from sot_ipython_connection.sot_client import SOTClient


def main():
    # TODO: launch the qt client
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication([])

    kernel_client = SOTClient()
    kernel_client.run_python_command("a = {'a': 1, 'b': 2}")
    kernel_client.run_python_command("a")
    kernel_client.show_history()


if __name__ == "__main__":
    main()
