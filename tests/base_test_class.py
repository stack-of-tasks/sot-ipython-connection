from unittest import TestCase
from time import sleep
from pathlib import Path

from sot_ipython_connection.sot_kernel import SOTKernel


input_scripts_dir = str(Path(__file__).resolve().parent/'input_scripts')


"""
    FIXME:

    If a SOTKernel is already running, another cannot be launched because it would
    use the same ports (this is expected behavior).

    First bug:
    When running these tests when a SOTKernel is already running, it should fail because
    this class launches its own SOTKernel. But the tests are run anyway because the exception
    when launching the kernel is ignored, and each test class launches a client that
    connect to the latest SOTKernel (i.e the one launched before the tests).

    Second bug:
    When there is no SOTKernel running, the tests crash after the first one is completed,
    and the SOTKernel's ports are not closed. When the tests are run again without having
    closed the ports, they work because their clients connect to the kernel whose ports
    were not closed (same reason as the first bug).
"""


class BaseTestClass(TestCase):

    # @classmethod
    # def setup_class(self):
    #     # Launching the kernel in a subprocess
    #     self._kernel = SOTKernel()
    #     self._kernel.run_non_blocking()

    # @classmethod
    # def teardown_class(self):
    #     # Terminating the kernel's subprocess
    #     del self._kernel
    #     sleep(1)

    def setup_method(self, method):
        write_in_logs('setup_method\n')
        # Launching the kernel in a subprocess
        self._kernel = SOTKernel()
        self._kernel.run_non_blocking()
        sleep(1)


    def teardown_method(self, method):
        write_in_logs('teardown_method\n')
        # Terminating the kernel's subprocess
        del self._kernel
        sleep(1)


def write_in_logs(str):
    with open('logs', 'a') as f:
        f.write(str)