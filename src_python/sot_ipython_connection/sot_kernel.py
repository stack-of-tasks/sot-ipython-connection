from time import sleep
from typing import Dict

from ipykernel.kernelapp import launch_new_instance

from sot_ipython_connection.connection_config import connection_config
from sot_ipython_connection.kernel_namespace_config import kernel_namespace

class SOTKernel:
    """ A configurable ipython kernel to work with the Stack of Tasks. """
    
    def __init__(self):
        # The kernel's connection information (ports, ip...).
        # Configurable in connection_config.py:
        self._connectionConfig: Dict = connection_config
        # TODO: error management if no file

        # The variables the kernel will be initialized with when launched.
        # Configurable in kernel_namespace_config.py:
        self._namespace: Dict = kernel_namespace
        # TODO: error management if no file

        # Pid of the subprocess the kernel is launched in in case of a non-blocking run:
        self._kernel_pid = None


    def run(self) -> None:
        """ Launches a new instance of a kernel, with the configured
            namespace and ports. This is a blocking call.
        """
        # List of the kernel's options:
        # https://ipython.readthedocs.io/en/7.23.0/config/options/kernel.html
        launch_new_instance(
            user_ns = self._namespace,
            shell_port = self._connectionConfig.get("shell_port"),
            iopub_port = self._connectionConfig.get("iopub_port"),
            stdin_port = self._connectionConfig.get("stdin_port"),
            control_port = self._connectionConfig.get("control_port"),
            hb_port = self._connectionConfig.get("hb_port"),
            ip = self._connectionConfig.get("ip"),
            transport = self._connectionConfig.get("transport"),
            signature_scheme = self._connectionConfig.get("signature_scheme")
        )


    def run_non_blocking(self) -> None:
        """ Launches a new instance of a kernel, with the configured
            namespace and ports, in a subprocess. This subprocess is terminated
            when the `SOTKernel` object is destroyed.
        """
        ... # allow only one run 


    def __del__(self):
        ...
        # if self._kernel_pid is not None:
        #     for _ range(5):
        #         if self._kernel_pid.is_alive():
        #             self._kernel_pid.terminate()
        #             sleep(0.1)
        #         else:
        #             break
        #     if self._kernel_pid.is_alive():
        #         for _ range(5):
        #         if self._kernel_pid.is_alive():
        #             self._kernel_pid.kill()
        #             sleep(0.1)
        #         else:
        #             break
        #     self._kernel_pid.join()
