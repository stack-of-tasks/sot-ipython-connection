import sys

from sot_ipython_connection.sot_client import SOTClient


def main(scripts_paths):
    kernel_client = SOTClient()

    # Running every script
    for path in scripts_paths:
        kernel_client.run_python_script(path)


if __name__ == "__main__":
    assert len(sys.argv) > 1
    main(sys.argv[1:])