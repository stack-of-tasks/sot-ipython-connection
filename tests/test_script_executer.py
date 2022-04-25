import os
import time
from subprocess import Popen

from sot_ipython_connection.sot_client import SOTClient
from sot_ipython_connection.app.sot_script_executer import main as script_executer


script_directory = os.path.dirname(__file__)


class TestScriptExecuter:

    @classmethod
    def setup_class(self):
        # Launching the kernel in a subprocess
        interpreter_path = os.path.join(
            os.path.dirname(__file__),
            '../src_python/sot_ipython_connection/app/sot_interpreter.py'
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

        script_executer([script_directory + "/script_test_1.py"])
        kernel_client.run_python_command("script_var_1")
        kernel_client.run_python_command("script_var_2")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None

        assert kernel_client.cmd_history[0].result == 1
        assert kernel_client.cmd_history[1].result == 2


    def test_multiple_scripts_var_definition(self):
        kernel_client = SOTClient()

        script_executer([script_directory + "/script_test_2.py",
            script_directory + "/script_test_3.py"])
        kernel_client.run_python_command("script_var_3")
        kernel_client.run_python_command("script_var_4")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None

        assert kernel_client.cmd_history[0].result == 3
        assert kernel_client.cmd_history[1].result == 4


    def test_multiple_scripts_var_redefinition(self):
        kernel_client = SOTClient()

        script_executer([script_directory + "/script_test_4.py",
            script_directory + "/script_test_5.py"])
        kernel_client.run_python_command("script_var_5")
        kernel_client.run_python_command("script_var_6")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None

        assert kernel_client.cmd_history[0].result == 55
        assert kernel_client.cmd_history[1].result == 6
