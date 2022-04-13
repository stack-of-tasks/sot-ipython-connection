from ipykernel.kernelapp import launch_new_instance
import os

def main():
    # The IPython kernel's user namespace will be initialized with the
    # variables contained in this dictionary:
    namespace = dict(
        a = 0,
        b = 54
    )

    # Kernel options:
    # https://ipython.readthedocs.io/en/7.23.0/config/options/kernel.html
    launch_new_instance(
        user_ns = namespace,
        #connection_file = "kernel-16975.json" # Does not work
        #ipython_dir = os.getcwd() + '/kernel/.ipython', # Does not work
        shell_port = 42767,
        iopub_port = 46117,
        stdin_port = 38481,
        control_port = 9872,
        hb_port = 52277,
        ip = "127.0.0.1",
        #key = "cac9bdce-78993a62b728ed3411b6bf97", Does not work
        transport = "tcp",
        signature_scheme = "hmac-sha256",
        #kernel_name = "sot" # Does not work
    )

    # TODO: try to change the port
    # 

if __name__ == "__main__" :
    main()
