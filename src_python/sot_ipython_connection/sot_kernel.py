from time import sleep
from typing import Dict
from multiprocessing import Process

from ipykernel.kernelapp import launch_new_instance

from sot_ipython_connection.connection_config import connection_config
from sot_ipython_connection.kernel_namespace_config import kernel_namespace
from sot_ipython_connection.sot_client import SOTClient

class SOTKernel:
    """ A configurable ipython kernel to work with the Stack of Tasks. """
    
    def __init__(self):

        # The kernel's connection information (ports, ip...).
        # Configurable in connection_config.py:
        self._connectionConfig: Dict = connection_config

        # Checking if all the required options are in self._connectionConfig:
        required_options = ["shell_port", "iopub_port", "stdin_port", "control_port",
            "hb_port", "ip", "transport", "signature_scheme"]
        for option in required_options:
            if option not in self._connectionConfig:
                raise KeyError(f"{option} could not be found in connection_config.py")

        # The variables the kernel will be initialized with when launched.
        # Configurable in kernel_namespace_config.py:
        self._namespace: Dict = kernel_namespace

        # Subprocess the kernel is launched in in case of a non-blocking run:
        self._process = None


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

        # Only one instance of the kernel can run at a time:
        if self._process is not None:
            print('A non-blocking instance of this kernel is already running.')
            return
        
        # Launching a new instance in another process.
        # Thanks to the daemon option, when the parent process exits, it will try to
        # terminate the child process (in case the parent is not properly stopped and
        # __del__ is not called)
        self._process = Process(target=self.run, daemon=True, name='sotkernel')
        self._process.start()

        # Waiting for the process to start:
        while not self._process.is_alive():
            sleep(0.001)

        # Waiting for the kernel's ports to open:
        local_client = SOTClient()
        while not local_client.connect_to_kernel():
            sleep(0.001)
        del local_client


    def stop_non_blocking(self):
        """ Terminates the subprocess in which the kernel is running, if any. """
        if self._subprocess_kernel_is_running():
            self._terminate_kernel_subprocess()


    def _terminate_kernel_subprocess(self) -> None:
        """ Terminates the subprocess in which the kernel is running. """
        if self._process.is_alive():
            self._process.terminate()
            self._process.join()
            if self._process.is_alive():
                self._process.kill()
                self._process.join()

        
    def _subprocess_kernel_is_running(self) -> bool:
        """ Returns True if there is an instance of this kernel currently running
            in another process.
        """
        # Cheking if a subprocess was launched:
        if self._process is None:
            return False

        return self._process.is_alive()


    def __del__(self):
        self.stop_non_blocking()
