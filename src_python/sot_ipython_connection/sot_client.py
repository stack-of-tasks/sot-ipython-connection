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

""" Documentation on messaging with jupyter:
    https://jupyter-client.readthedocs.io/en/latest/messaging.html#messaging-in-jupyter

    Documentation on BlockingKernelClient:
    https://www.adamsmith.haus/python/docs/jupyter_client.BlockingKernelClient
"""


class SOTCommandInfo:
    session = None # To know which client has sent the command
    cmd = None
    result = None
    stdout = None
    stderr = None


class SOTClient(BlockingKernelClient):
    def __init__(self):
        # List of SOTCommandInfo: history of every received response
        # (triggered by a command from this client or another)
        self.cmd_history = []

        # Setting up and starting the communication with the kernel
        self.load_connection_file(get_latest_connection_file_path())
        self.start_channels()


    def is_response_to_self(self, response):
        """ Is the given response responding to a request sent by this
            client ?
        """
        return True
        # TODO: see if the session's id can be retreived
        # and compare it to the one in the parent_header


    def get_self_history(self):
        """ Returns a filtered copy of self.cmd_history by keeping
            only the commands that were sent by this client
        """
        ... # TODO -> use self.is_response_to_self()


    def save_command_info(self, response):
        ...


    def run_python_command(self, cmd):
        """ This is a blocking function that sends a command to the
            kernel and waits for it to respond completely (see link
            to the doc on messaging with jupyter for the steps),
            while saving every response it gets to self.cmd_history
        """

        # Sending the command to the kernel
        msg_id = self.execute(cmd)

        whole_response_received = False
        while not whole_response_received:
            try:
                # iopub is the channel where the kernel broadcasts side-effects
                # (stderr, stdout, debugging events, its status: busy or idle, etc)
                response = self.get_iopub_msg()
                
                # Printing the response if it's responding to OUR command
                if self.is_response_to_self(response):
                    print(response)
                    print()

                # Saving the response to the command history
                self.save_command_info(response)

                # We can stop listening to the kernel's responses if it
                # changes its status to 'idle' in response to OUR command.
                # (parent_header is the header of the message the kernel is
                # responding to)
                if response["content"]["execution_state"] == "idle" \
                    and response["parent_header"]["msg_id"] == msg_id:
                    whole_response_received = True
            except:
                ...


    def run_python_script(self, filepath):
        self.run_python_command("%run " + str(filepath))


    def __del__(self):
        self.stop_channels()
