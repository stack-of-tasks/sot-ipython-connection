import IPython
from ipykernel.kernelapp import launch_new_instance
from ipykernel.kernelbase import Kernel
from ipykernel.kernelapp import IPKernelApp as IPKA
from traitlets.config import Config

def main():
    # 1st try:
    # Using the ipython_config and ipython_kernel_config files by setting
    # c.InteractiveShellApp.exec_lines and c.TerminalIPythonApp.exec_lines
    #launch_new_instance()

    # 2nd try (successful):
    # ~/.ipython/profile_default/startup/init_lsst.py will be
    # executed during IPython setup
    #launch_new_instance()

    # 3rd try:
    # https://ipython.readthedocs.io/en/7.x/api/generated/IPython.html?highlight=kernel#IPython.start_kernel
    # The IPython user namespace will be initialized with these variables:
    namespace = dict(
        a = 0,
        b = 54
    )
    launch_new_instance(user_ns=namespace)

    # 4th try:
    """ namespace = dict(
        a = 0,
        b = 54
    )
    app = IPKA.instance()
    app.initialize([])
    app.kernel.user_ns = namespace
    app.start() """

    # 5th try:
    # https://ipython.readthedocs.io/en/stable/config/intro.html#running-ipython-from-python
    """ c = Config()
    c.InteractiveShellApp.exec_lines = ["pppp = 555"]
    c.InteractiveShellApp.init_code()
    print(IPKA.connection_file)
    IPython.start_kernel(config=c) """

    # 6th try:
    # https://ipython.readthedocs.io/en/7.x/config/intro.html#command-line-arguments

    # 7th try:
    # https://ipython.readthedocs.io/en/7.x/config/intro.html#the-ipython-directory
    # Launching the launch_ipython_kernel script

    # 8th try:
    """ my_kernel = IPKA.instance()
    my_kernel.initialize()
    my_kernel.user_ns = dict(test5 = 5)
    my_kernel.start() """

    # 9th try:
    """ test = 41
    IPython.embed_kernel(local_ns=dict(test2 = 3, test3 = 4)) """
 

if __name__ == "__main__" :
    main()
