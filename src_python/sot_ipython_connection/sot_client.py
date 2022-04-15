from operator import truediv
from pathlib import Path
import nest_asyncio
import jupyter_core
from jupyter_client import BlockingKernelClient


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


class SOTClient(BlockingKernelClient):
    def __init__(self):
        self.load_connection_file(get_latest_connection_file_path())
        self.start_channels()

    def run_python_command(self, cmd):
        # Documentation on messaging with jupyter:
        # https://jupyter-client.readthedocs.io/en/latest/messaging.html#messaging-in-jupyter
        
        # Sending the command to the kernel
        msg_id = self.execute(cmd)

        whole_response_received = False
        while not whole_response_received:
            try:
                # iopub is the channel where the kernel broadcasts side-effects
                # (stderr, stdout, debugging events, its status: busy or idle, etc)
                response = self.get_iopub_msg()
                print(response)
                print()

                # We can stop listening to the kernel's responses if it
                # changes its status to 'idle' in response to OUR command.
                # (parent_header is the header of the message the kernel is
                # responding to)
                if response["content"]["execution_state"] == "idle" \
                    and response["parent_header"]["msg_id"] == msg_id:
                    whole_response_received = True
            except:
                ...
        
        # TODO: return un SOTClientOut, le save dans une liste pour faire
        # un historique

    def run_python_script(self, filepath):
        self.run_python_command("%run " + str(filepath))

    def __del__(self):
        self.stop_channels()
