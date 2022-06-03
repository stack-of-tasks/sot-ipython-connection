from unittest import TestCase
from time import sleep
from pathlib import Path

from sot_ipython_connection.sot_kernel import SOTKernel


input_scripts_dir = str(Path(__file__).resolve().parent/'input_scripts')


class BaseTestClass(TestCase):

    @classmethod
    def setup_class(self):
        # Launching the kernel in a subprocess
        self._kernel = SOTKernel()
        self._kernel.run_non_blocking()

    @classmethod
    def teardown_class(self):
        # Terminating the kernel's subprocess
        del self._kernel
        sleep(1)
    