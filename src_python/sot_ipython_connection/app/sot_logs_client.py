from PyQt5 import QtWidgets

from sot_ipython_connection.sot_client import SOTClient


def main():
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication([])

    kernel_client = SOTClient()

    exit_requested = False

    while not exit_requested:
        #user_input = input()
        #if user_input in ["exit", "quit", "exit()", "quit()"]:
        #    exit_requested = True

        try:
            print("try")
            # iopub is the channel where the kernel broadcasts side-effects
            # (stderr, stdout, debugging events, its status: busy or idle, etc)
            # to every client connected to it
            response = kernel_client.get_iopub_msg()
            print(response)

            # Saving the response to the command history
            cmd = kernel_client.save_response(response)

            # Displaying the command if the kernel has finished reponding to it
            # TODO

        except: # Entered when there is reponse to read
            ...


if __name__ == "__main__":
    main()