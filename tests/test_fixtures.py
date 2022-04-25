import os
import pytest
from subprocess import Popen

@pytest.fixture(autouse=True)
def launch_kernel_and_app():
    # Launching the kernel in a subprocess
    interpreter_path = os.path.join(
       os.path.dirname(__file__),
       '../src_python/sot_ipython_connection/app/sot_interpreter.py'
    )
    kernel_process = Popen(["python3", interpreter_path])
    kernel_process.wait(10)

    # Running the tests
    yield

    # Terminating and killing the kernel's subprocess
    kernel_process.terminate()
    kernel_process.wait(10)
    kernel_process.kill()
    kernel_process.wait(10)