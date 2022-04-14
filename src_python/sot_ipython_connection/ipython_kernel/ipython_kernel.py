import os
import sys
from ipykernel.kernelapp import launch_new_instance

def main():

    # Importing the connection configuration (../connectionConfig)
    scriptDirectory = os.path.dirname(__file__)
    moduleDirectory = os.path.join(scriptDirectory, '..')
    sys.path.append(moduleDirectory)
    import connection_config
    connectionConfig = connection_config.config

    # The IPython kernel's user namespace will be initialized with the
    # variables contained in this dictionary:
    namespace = dict(
        a = 0,
        b = 54
    )

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
