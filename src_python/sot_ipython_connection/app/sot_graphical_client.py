from PyQt5 import QtWidgets

from sot_ipython_connection.sot_client import SOTClient


def main():
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication([])

    kernel_client = SOTClient()
    kernel_client.run_python_command("print('azerty')")
    kernel_client.print_history()


if __name__ == "__main__":
    main()
