""" import os

from subprocess import Popen


def main():
    # Launching the kernel in a subprocess
    kernel_launch_cmd = ["python3", "src_python/sot_ipython_connection/app/sot_interpreter.py"]
    kernel_process = Popen(kernel_launch_cmd)
    print(kernel_process.pid)

    # Killing the kernel's subprocess
    kernel_process.wait(10000)
    print("1")
    kernel_process.terminate()
    print("2")
    kernel_process.wait(10000)
    print("3")
    kernel_process.kill()
    print("4")


if __name__ == "__main__":
    main() """

""" from sot_ipython_connection.sot_client import SOTCommandInfo


def main():
    cmd_error = SOTCommandInfo.SOTCommandError()
    cmd_error.traceback  = "ghkfg"
    cmd_error.name = "jkhg"
    cmd_error.value = "lkgl"

    print(str(cmd_error))


if __name__ == "__main__":
    main() """

class cmd_test_class:
    def __init__(self, attr_1):
        self.attr_1 = attr_1
        self.attr_2 = 2
        self.attr_3 = 3

