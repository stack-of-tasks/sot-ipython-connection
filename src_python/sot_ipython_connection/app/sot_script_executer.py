import sys
import os

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from sot_client import SOTClient


def main(scripts_paths):
    kernel_client = SOTClient()

    # Running every script
    for path in scripts_paths:
        kernel_client.run_python_script(path)


if __name__ == "__main__":
    assert len(sys.argv) > 1
    main(sys.argv[1:])