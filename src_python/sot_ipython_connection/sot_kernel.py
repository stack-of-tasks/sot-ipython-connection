import os
import sys
from ipykernel.kernelapp import launch_new_instance


class SOTKernel:
    """ A configurable ipython kernel to work with the Stack of Tasks.
        - self.connectionConfig (dict): the kernel's connection info
          (ports, ip...). Configurable in `connection_config.py`.
        - self.namespace (dict): the variables the kernel will be
          initialized with when launched. Configurable in
          `kernel_namespace_config.py`.
    """
    
    def __init__(self):
        # Importing the connection and namespace configurations
        scriptDirectory = os.path.dirname(__file__)
        moduleDirectory = os.path.join(scriptDirectory, '..')
        sys.path.append(moduleDirectory)
        import connection_config
        import kernel_namespace_config

        self.connectionConfig = connection_config.config
        # TODO: error management if no file

        self.namespace = kernel_namespace_config.kernel_namespace
        # TODO: error management if no file

    def run(self):
        """ Launches a new instance of a kernel, with the configured
            namespace and ports.
        """
        # List of the kernel's options:
        # https://ipython.readthedocs.io/en/7.23.0/config/options/kernel.html
        launch_new_instance(
            user_ns = self.namespace,
            shell_port = self.connectionConfig["shell_port"],
            iopub_port = self.connectionConfig["iopub_port"],
            stdin_port = self.connectionConfig["stdin_port"],
            control_port = self.connectionConfig["control_port"],
            hb_port = self.connectionConfig["hb_port"],
            ip = self.connectionConfig["ip"],
            transport = self.connectionConfig["transport"],
            signature_scheme = self.connectionConfig["signature_scheme"]
        )
