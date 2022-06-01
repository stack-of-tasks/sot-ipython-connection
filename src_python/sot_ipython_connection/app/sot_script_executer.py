import sys

from argparse import ArgumentParser
from turtle import Vec2D
from typing import List

from sot_ipython_connection.sot_client import SOTClient


def main(arguments):

    # Parsing the arguments to get the list of filepaths and the --local option (bool)
    arg_parser = ArgumentParser(
        description='Execute one or several python scripts on the latest SOTKernel.',
        epilog="The scripts will be executed in the same order as they are given to \
            the program. Their paths can be relative or absolute."
    )
    arg_parser.add_argument('script_paths', type=str, nargs='+',
        help='Path of a script to execute in the kernel')
    arg_parser.add_argument('--local', dest='local', action='store_const',
        const=True, default=False,
        help='Use this option if the scripts to execute are located \
            on the same machine as the client. Otherwise, they will be considered \
            to be on the same machine as the kernel.')
    args = arg_parser.parse_args(arguments)

    scripts_are_local: bool = args.local
    scripts_paths: List[str] = args.script_paths

    kernel_client = SOTClient()
    
    # The function used to execute the scripts depends on if the scripts are local
    if scripts_are_local:
        run_python_script = kernel_client.run_local_python_script
    else:
        run_python_script = kernel_client.run_kernel_side_python_script
    
    # Running every script
    for path in scripts_paths:
        run_python_script(path)


if __name__ == "__main__":
    main(sys.argv[1:])