from pathlib import Path
import nest_asyncio
import jupyter_core
from qtconsole.client import QtKernelClient


nest_asyncio.apply()


def get_latest_connection_file_path():
    directory_path = Path(jupyter_core.paths.jupyter_runtime_dir())
    files = directory_path.glob("*")
    return max(files, key=lambda x: x.stat().st_ctime)


class SOTClientOut:
    cmd = None
    result = None
    stdout = None
    stderr = None


class SOTClient(QtKernelClient):
    def __init__(self):
        self.load_connection_file(get_latest_connection_file_path())
        self.start_channels()

    def run_python_command(self, cmd):
        result = self.execute(cmd)
        # TODO: return stderr, stdout, result à l'envers, les save avec
        # la cmd dans une var / liste pour un historique : SOTClientOut

    def run_python_script(self, filepath):
        self.run_python_command("%run " + str(filepath))

    def __del__(self):
        self.stop_channels()
