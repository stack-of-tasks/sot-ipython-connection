from unittest import TestCase
import time
from subprocess import Popen

from pathlib import Path

from sot_ipython_connection.sot_client import SOTClient


class TestInitialNamespace(TestCase):

    @classmethod
    def setup_class(self):
        # Launching the kernel in a subprocess
        interpreter_path = (
            Path(__file__).resolve().parent.parent/
                'src_python'/'sot_ipython_connection'/'app'/'sot_interpreter.py'
        )
        self.kernel_process = Popen(["python3", interpreter_path])
        time.sleep(5)

    @classmethod
    def teardown_class(self):
        # Terminating and killing the kernel's subprocess
        self.kernel_process.terminate()
        self.kernel_process.wait(10)
        self.kernel_process.kill()
        self.kernel_process.wait(10)


    def test_namespace(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("initial_namespace_1")
        kernel_client.run_python_command("initial_namespace_2")
        kernel_client.run_python_command("initial_namespace_1 + initial_namespace_2")
        kernel_client.run_python_command("initial_namespace_3")

        assert len(kernel_client.cmd_history) == 4

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None
        assert kernel_client.cmd_history[2].stderr == None
        assert kernel_client.cmd_history[3].stderr != None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None
        assert kernel_client.cmd_history[2].stdout == None
        assert kernel_client.cmd_history[3].stdout == None

        assert kernel_client.cmd_history[0].result == 46
        assert kernel_client.cmd_history[1].result == 54
        assert kernel_client.cmd_history[2].result == 100
        assert kernel_client.cmd_history[3].result == None
