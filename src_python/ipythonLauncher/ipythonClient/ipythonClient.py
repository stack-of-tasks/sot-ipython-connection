
import sys
from qtconsole.client import QtKernelClient
import jupyter_core
import nest_asyncio


class KernelClient:
    def __init__(self, kernel_number):
        self.kernel_client = QtKernelClient()
        if len(sys.argv) == 1:
            exit()
        self.kernel_client.load_connection_file(jupyter_core.paths.jupyter_runtime_dir() +
            '/kernel-' + kernel_number + '.json')
        self.kernel_client.start_channels()

    def run_python_command(self, cmd):
        self.kernel_client.execute(cmd, silent=False)

    #def __del__(self):
        # self.kernel_client.stop_channels()


def main(kernel_number, cmd):
    client = KernelClient(kernel_number)
    client.run_python_command(cmd)

if __name__ == "__main__":
    assert len(sys.argv) == 3
    nest_asyncio.apply()
    main(sys.argv[1], sys.argv[2])