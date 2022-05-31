from unittest import TestCase
import time
from subprocess import Popen

from pathlib import Path

from sot_ipython_connection.sot_client import SOTClient


class TestCommands(TestCase):

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


    def test_var_definition(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("cmd_1 = 1")
        kernel_client.run_python_command("cmd_2 = \"abc\"")
        kernel_client.run_python_command("cmd_1")
        kernel_client.run_python_command("cmd_2")

        assert len(kernel_client.cmd_history) == 4

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None
        assert kernel_client.cmd_history[2].stderr == None
        assert kernel_client.cmd_history[3].stderr == None
        
        assert kernel_client.cmd_history[2].stdout == None
        assert kernel_client.cmd_history[3].stdout == None
        
        assert kernel_client.cmd_history[2].result == 1
        assert kernel_client.cmd_history[3].result == 'abc'


    def test_var_redefinition(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("cmd_3 = 3")
        kernel_client.run_python_command("cmd_3 = 33")
        kernel_client.run_python_command("cmd_3")

        assert len(kernel_client.cmd_history) == 3

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None
        assert kernel_client.cmd_history[2].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None
        assert kernel_client.cmd_history[2].stdout == None

        assert kernel_client.cmd_history[0].result == None
        assert kernel_client.cmd_history[1].result == None
        assert kernel_client.cmd_history[2].result == 33


    def test_operations(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("cmd_4 = 4")
        kernel_client.run_python_command("cmd_5 = 5")
        kernel_client.run_python_command("cmd_6 = cmd_4 + cmd_5")
        kernel_client.run_python_command("cmd_6")

        assert len(kernel_client.cmd_history) == 4

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None
        assert kernel_client.cmd_history[2].stderr == None
        assert kernel_client.cmd_history[3].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None
        assert kernel_client.cmd_history[2].stdout == None
        assert kernel_client.cmd_history[3].stdout == None

        assert kernel_client.cmd_history[0].result == None
        assert kernel_client.cmd_history[1].result == None
        assert kernel_client.cmd_history[2].result == None
        assert kernel_client.cmd_history[3].result == 9
        

    def test_undefined_var(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("undefined_var")

        assert len(kernel_client.cmd_history) == 1
        assert kernel_client.cmd_history[0].stderr != None
        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[0].result == None
        

    def test_import(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("import math")
        kernel_client.run_python_command("fabs(-4)")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None

        assert kernel_client.cmd_history[0].result == None
        assert kernel_client.cmd_history[1].result == 4.0
        

    def test_object(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("\
            class cmd_test_class:\n \
                \tdef __init__(self, attr_1):\n \
                    \t\tself.attr_1 = attr_1\n \
                    \t\tself.attr_2 = 2\n \
                    \t\tself.attr_3 = 3\n \
        ")

        kernel_client.run_python_command("obj_1 = cmd_test_class(\"abc\")")
        kernel_client.run_python_command("obj_1.attr_3 = 33")
        kernel_client.run_python_command("obj_1.attr_1")
        kernel_client.run_python_command("obj_1.attr_2")
        kernel_client.run_python_command("obj_1.attr_3")

        assert len(kernel_client.cmd_history) == 6

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None
        assert kernel_client.cmd_history[2].stderr == None
        assert kernel_client.cmd_history[3].stderr == None
        assert kernel_client.cmd_history[4].stderr == None
        assert kernel_client.cmd_history[5].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None
        assert kernel_client.cmd_history[2].stdout == None
        assert kernel_client.cmd_history[3].stdout == None
        assert kernel_client.cmd_history[4].stdout == None
        assert kernel_client.cmd_history[5].stdout == None

        assert kernel_client.cmd_history[0].result == None
        assert kernel_client.cmd_history[1].result == None
        assert kernel_client.cmd_history[2].result == None
        assert kernel_client.cmd_history[3].result == 'abc'
        assert kernel_client.cmd_history[4].result == 2
        assert kernel_client.cmd_history[5].result == 33
