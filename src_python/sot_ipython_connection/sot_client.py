
import sys

from pathlib import Path
import nest_asyncio
import jupyter_core
from PyQt5 import QtWidgets
from qtconsole.client import QtKernelClient

nest_asyncio.apply()

class SOTClientOut:
    cmd = None
    result = None
    stdout = None
    stderr = None

def getLatestFile(path: Path, pattern: str = "*"): # TODO
    files = path.glob(pattern)
    return max(files, key=lambda x: x.stat().st_ctime)

class SOTClient(QtKernelClient):
    def __init__(self, kernel_number):
        self.load_connection_file(jupyter_core.paths.jupyter_runtime_dir() +
            '/kernel-' + kernel_number + '.json')
        self.start_channels()

    def run_python_command(self, cmd):
        self.execute(cmd, silent=False)
        # TODO: return stderr, stdout, result à l'envers, les save avec
        # la cmd dans une var / liste pour un historique : SOTClientOut

    def run_python_script(self, filepath):
        self.run_python_command("%run " + str(filepath))

    def __del__(self):
        self.stop_channels()


def main(kernel_number, cmd1):
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication(["test"])

    kernel_client = SOTClient(kernel_number)
    kernel_client.execute(cmd1, silent=False)


if __name__ == "__main__":
    assert len(sys.argv) == 3
    main(sys.argv[1], sys.argv[2])