from unittest import TestCase
from time import sleep
from pathlib import Path

from sot_ipython_connection.sot_kernel import SOTKernel


input_scripts_dir = str(Path(__file__).resolve().parent/'input_scripts')


""" FIXME:

    If a SOTKernel is already running, another cannot be launched because it would
    use the same ports (this is expected behavior).

    When running these tests when a SOTKernel is already running, it should fail because
    this class launches its own SOTKernel. But the tests are run anyway because the exception
    when launching the kernel is ignored, and each test class launches a client that
    connect to the latest SOTKernel (i.e the one launched before the tests).
"""


class BaseTestClass(TestCase):

    def setUp(self):
        # Launching the kernel in a subprocess
        self._kernel = SOTKernel()
        self._kernel.run_non_blocking()

    def tearDown(self):
        # Terminating the kernel's subprocess
        self._kernel.stop_non_blocking()
