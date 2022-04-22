from PyQt5 import QtWidgets

from sot_ipython_connection.sot_client import SOTClient


def main():
    # TODO: launch the qt client
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication([])

    kernel_client = SOTClient()
    kernel_client.run_python_command("print(\"azerty\\n\")")
    kernel_client.run_python_command("1+1")
    kernel_client.run_python_command("dfghjk")
    kernel_client.show_history()


if __name__ == "__main__":
    main()
