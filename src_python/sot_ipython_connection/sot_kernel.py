import os
import sys
from ipykernel.kernelapp import launch_new_instance


class SOTKernel:
    def __init__(self):
        # TODO: use Path
        # Importing the connection and namespace configurations
        scriptDirectory = os.path.dirname(__file__)
        moduleDirectory = os.path.join(scriptDirectory, '..')
        sys.path.append(moduleDirectory)
        import connection_config
        import kernel_namespace_config

        # The kernel's connection info (ports, ip...)
        self.connectionConfig = connection_config.config

        # The kernel's user namespace will be initialized with the
        # variables contained in this dictionary:
        self.namespace = kernel_namespace_config.kernel_namespace

    def run(self):
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


def main():
    kernel = SOTKernel()
    kernel.run()
    

if __name__ == "__main__" :
    main()
