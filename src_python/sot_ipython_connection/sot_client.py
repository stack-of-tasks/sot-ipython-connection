from pathlib import Path
import nest_asyncio
import jupyter_core
from jupyter_client import BlockingKernelClient



""" Documentation on messaging with jupyter:
    https://jupyter-client.readthedocs.io/en/latest/messaging.html#messaging-in-jupyter

    Documentation on BlockingKernelClient:
    https://www.adamsmith.haus/python/docs/jupyter_client.BlockingKernelClient
"""


nest_asyncio.apply()


def get_latest_connection_file_path():
    directory_path = Path(jupyter_core.paths.jupyter_runtime_dir())
    files = directory_path.glob("*")
    return max(files, key=lambda x: x.stat().st_ctime)


class SOTCommandInfo:
    def __init__(self):
        self.session_id = None # To know which client has sent the command
        self.id = None
        self.content = None
        self.stdout = None
        self.stderr = None # {traceback, ename, evalue}


class SOTClient(BlockingKernelClient):
    def __init__(self):
        self.session_id = self.session.session

        # List of SOTCommandInfo: history of this session's commands and their responses
        self.cmd_history = []
        """ TODO: the get_iopub_msg() call used in this program returns responses to
            every client (session) connected to the kernel.
            To store a history of every session's commands, we should listen to the kernel's
            iopub channel in another thread and save the commands with the method currently 
            used, as self.save_command_info() already saves the command's session id (which
            allows to differentiate every client)
            self.get_self_history currently has no use, as self.cmd_history only store this
            session's commands.
        """

        # Setting up and starting the communication with the kernel
        self.load_connection_file(get_latest_connection_file_path())
        self.start_channels()


    def is_response_to_self(self, response):
        """ Is the given response responding to a request sent by this
            session?
        """
        if self.session_id == response["parent_header"]["session"]:
            return True


    def save_command_info(self, response):
        # Creating the command if it's its first response
        cmd = self.get_cmd_by_id(response["parent_header"]["msg_id"])
        is_new_cmd = False

        if cmd == None:
            is_new_cmd = True
            cmd = SOTCommandInfo()
            cmd.session_id = response["parent_header"]["session"]
            cmd.id = response["parent_header"]["msg_id"]
        
        # Saving the command's content
        if response["msg_type"] == "execute_input":
            cmd.content = response["content"]["code"]

        # Saving the command's output if applicable
        if response["msg_type"] == "execute_result":
            cmd.stdout = response["content"]["data"]["text/plain"]

        # Saving the command's error if applicable
        if response["msg_type"] == "error":
            cmd.stderr = response["content"]

        if is_new_cmd:
            self.cmd_history.append(cmd)


    def get_cmd_by_id(self, id):
        for cmd in reversed(self.cmd_history):
            if cmd.id == id:
                return cmd
        return None


    def show_history(self, history=None):
        if history == None:
            history = self.cmd_history

        for cmd in history:
            print("session_id:", cmd.session_id)
            print("id:", cmd.id)
            print("content:", cmd.content)
            print("stdout:", cmd.stdout)
            print("stderr:", cmd.stderr)
            print()


    def show_self_history(self):
        self_history = self.get_self_history()
        self.show_history(self_history)


    def get_self_history(self):
        """ Returns a filtered copy of self.cmd_history by keeping
            only the commands that were sent by this session
        """
        self_history = []
        for cmd in self.cmd_history:
            if cmd.session_id == self.session_id:
                self_history.append(cmd)


    def run_python_command(self, cmd):
        """ This is a blocking function that sends a command to the
            kernel and waits for it to respond completely (see link
            to the doc on messaging with jupyter for every step),
            while saving the response to self.cmd_history
        """

        # Sending the command to the kernel
        msg_id = self.execute(cmd)

        whole_response_received = False
        while not whole_response_received:
            try:
                # iopub is the channel where the kernel broadcasts side-effects
                # (stderr, stdout, debugging events, its status: busy or idle, etc)
                # to every client connected to it
                response = self.get_iopub_msg()

                # Saving the response to the command history only if it responds
                # to our command
                if response["parent_header"]["msg_id"] == msg_id:
                    self.save_command_info(response)

                # We can stop listening to the kernel's responses if it
                # changes its status to 'idle' in response to OUR command.
                if response["content"]["execution_state"] == "idle" \
                    and self.is_response_to_self(response):
                    whole_response_received = True

            except: # Entered when there is no more reponses to get
                ...


    def run_python_script(self, filepath):
        self.run_python_command("%run " + str(filepath))


    def __del__(self):
        self.stop_channels()
