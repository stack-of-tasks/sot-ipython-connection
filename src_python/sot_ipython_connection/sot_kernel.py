import os
import sys
from ipykernel.kernelapp import launch_new_instance


class SOTKernel:
    def __init__(self):
        ...


def main():
    
    # TODO: use Path
    # Importing the connection and namespace configurations
    scriptDirectory = os.path.dirname(__file__)
    moduleDirectory = os.path.join(scriptDirectory, '..')
    sys.path.append(moduleDirectory)
    import connection_config
    import kernel_namespace_config

    # The kernel's connection info (ports, ip...)
    connectionConfig = connection_config.config

    # The kernel's user namespace will be initialized with the
    # variables contained in this dictionary:
    namespace = kernel_namespace_config.kernel_namespace

    # List of the kernel's options:
    # https://ipython.readthedocs.io/en/7.23.0/config/options/kernel.html
    launch_new_instance(
        user_ns = namespace,
        shell_port = connectionConfig["shell_port"],
        iopub_port = connectionConfig["iopub_port"],
        stdin_port = connectionConfig["stdin_port"],
        control_port = connectionConfig["control_port"],
        hb_port = connectionConfig["hb_port"],
        ip = connectionConfig["ip"],
        transport = connectionConfig["transport"],
        signature_scheme = connectionConfig["signature_scheme"]
    )


if __name__ == "__main__" :
    main()
