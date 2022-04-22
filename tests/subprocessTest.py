import os

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
    main()