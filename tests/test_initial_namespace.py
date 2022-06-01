from unittest import TestCase

from sot_ipython_connection.sot_kernel import SOTKernel
from sot_ipython_connection.sot_client import SOTClient

import nest_asyncio
nest_asyncio.apply()


class TestInitialNamespace(TestCase):

    @classmethod
    def setup_class(self):
        # Launching the kernel in a subprocess
        self._kernel = SOTKernel()
        self._kernel.run_non_blocking()

    @classmethod
    def teardown_class(self):
        # Terminating the kernel's subprocess
        self._kernel._terminate_kernel_subprocess()


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
