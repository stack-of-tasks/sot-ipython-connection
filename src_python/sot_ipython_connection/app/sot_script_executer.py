import sys

from sot_ipython_connection.sot_client import SOTClient


def main(arguments):
    kernel_client = SOTClient()

    # If the local (-l or --local) option is used, we remove it from the arguments
    # so that only the script paths remain
    scripts_paths = arguments
    scripts_are_local = False
    if '-l' in arguments:
        scripts_are_local = True
        scripts_paths.pop(scripts_paths.index('-l'))
    elif '--local' in arguments:
        scripts_are_local = True
        scripts_paths.pop(scripts_paths.index('--local'))
    
    # The function used to execute the scripts depends on if the scripts are local
    if scripts_are_local:
        run_python_script = kernel_client.run_local_python_script
    else:
        run_python_script = kernel_client.run_kernel_side_python_script
    
    # Running every script
    for path in scripts_paths:
        run_python_script(path)


if __name__ == "__main__":
    
    # Displaying usage:
    if len(sys.argv) < 1 or '-h' in sys.argv or '--help' in sys.argv:
        print()
        print('USAGE:')
        print('./sot_script_executer [-l] scriptPath1 [scriptPath2 ...]')
        print()
        print('ARGUMENTS:')
        print("The scripts' paths can be relative or absolute (see more details below).")
        print("The script will be executed in the same order as they are given to this program.")
        print()
        print('OPTIONS:')
        print("-l or --local\tUse this option if the scripts to execute are located " +
            "on the same machine as the client. Otherwise, they will be considered " +
            "to be on the same machine as the kernel.")
        print()
        exit()

    main(sys.argv[1:])