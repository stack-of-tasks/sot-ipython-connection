from unittest import TestCase

from sot_ipython_connection.sot_kernel import SOTKernel
from src_python.sot_ipython_connection.sot_client import SOTClient, SOTCommandError

import nest_asyncio
nest_asyncio.apply()


class TestClientHistory(TestCase):

    @classmethod
    def setup_class(self):
        # Launching the kernel in a subprocess
        self._kernel = SOTKernel()
        self._kernel.run_non_blocking()

    @classmethod
    def teardown_class(self):
        # Terminating the kernel's subprocess
        self._kernel._terminate_kernel_subprocess()


    def test_no_cmd(self):
        kernel_client = SOTClient()
        assert len(kernel_client.cmd_history) == 0


    def test_one_cmd_successful(self):
        kernel_client = SOTClient()
        kernel_client.run_python_command("1 + 1")

        assert len(kernel_client.cmd_history) == 1

        assert kernel_client.cmd_history[0].session_id == kernel_client.session_id
        assert kernel_client.cmd_history[0].id != None
        assert kernel_client.cmd_history[0].content == "1 + 1"
        assert kernel_client.cmd_history[0].result == 2
        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[0].stderr == None


    def test_one_cmd_error(self):
        kernel_client = SOTClient()
        kernel_client.run_python_command("unknown_variable")

        assert len(kernel_client.cmd_history) == 1

        assert kernel_client.cmd_history[0].session_id == kernel_client.session_id
        assert kernel_client.cmd_history[0].id != None
        assert kernel_client.cmd_history[0].content == "unknown_variable"
        assert kernel_client.cmd_history[0].result == None
        assert kernel_client.cmd_history[0].stdout == None

        assert kernel_client.cmd_history[0].stderr != None
        assert isinstance(kernel_client.cmd_history[0].stderr, SOTCommandError)
        assert kernel_client.cmd_history[0].stderr.traceback != None
        assert isinstance(kernel_client.cmd_history[0].stderr.traceback, str)
        assert kernel_client.cmd_history[0].stderr.name != None
        assert isinstance(kernel_client.cmd_history[0].stderr.name, str)
        assert kernel_client.cmd_history[0].stderr.value != None
        assert isinstance(kernel_client.cmd_history[0].stderr.name, str)


    def test_one_cmd_stdout(self):
        kernel_client = SOTClient()

        kernel_client.run_python_command("print('hello')")

        assert len(kernel_client.cmd_history) == 1
        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[0].stdout == 'hello\n'
        assert kernel_client.cmd_history[0].result == None
        

    def test_several_cmd(self):
        kernel_client = SOTClient()
        kernel_client.run_python_command("test_history_1 = 1")
        kernel_client.run_python_command("test_history_1")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].session_id == kernel_client.session_id
        assert kernel_client.cmd_history[0].id != None
        assert kernel_client.cmd_history[0].content == "test_history_1 = 1"
        assert kernel_client.cmd_history[0].result == None
        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[0].stderr == None

        assert kernel_client.cmd_history[1].session_id == kernel_client.session_id
        assert kernel_client.cmd_history[1].id != None
        assert kernel_client.cmd_history[1].content == "test_history_1"
        assert kernel_client.cmd_history[1].result == 1
        assert kernel_client.cmd_history[1].stdout == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[1].id != kernel_client.cmd_history[0].id
        

    def test_several_sessions(self):
        ... # TODO
        

    def test_self_history(self):
        ...
        # TODO: compare history and self history after several clients
        # have sent commands
