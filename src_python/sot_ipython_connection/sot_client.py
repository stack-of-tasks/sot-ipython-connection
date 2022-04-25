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
    # TODO: error management if there is no file
    return max(files, key=lambda x: x.stat().st_ctime)


class SOTCommandInfo:
    class SOTCommandError:
        def __init__(self):
            self.traceback = None
            self.name = None
            self.value = None


    def __init__(self):
        self.session_id = None # To know which client has sent the command
        self.id = None
        self.content = None
        self.result = None
        self.stdout = None
        self.stderr = None # SOTCommandError


    def show_cmd(self):
        print("Session id:", self.session_id)
        print("Command id:", self.id)
        print("Command:")
        print(f"`{self.content}`")
        if self.result:
            print("Result:")
            print(type(self.result))
            print(self.result)
        if self.stdout:
            print("Output:")
            print(f"`{self.stdout}`")
        if self.stderr:
            print("Error output:")
            print(self.stderr.traceback)


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


    def is_kernel_alive(self):
        ...
        # TODO: listen to the kernel's heartbeat and return True if
        # the kernel is alive


    def reconnect_to_kernel(self):
        ...
        # TODO: Reconnect to the latest kernel


    def is_response_to_self(self, response):
        """ Is the given response responding to a request sent by this
            session?
        """
        if self.session_id == response["parent_header"]["session"]:
            return True

    # TODO: update tests (adding result, modifying stdout)
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

        # Saving the command's result
        if response["msg_type"] == "execute_result":
            try:
                # Trying to parse the response
                cmd.result = eval(response["content"]["data"]["text/plain"])
            except:
                # If the data is not parsable (e.g if it's a type), storing
                # the string
                cmd.result = response["content"]["data"]["text/plain"]
        # TODO: test it

        # Saving the command's stdout
        if response["msg_type"] == "stream":
            cmd.stdout = response["content"]["text"]

        # Saving the command's error
        if response["msg_type"] == "error":
            cmd.stderr = cmd.SOTCommandError()
            cmd.stderr.name = response["content"]["ename"]
            cmd.stderr.value = response["content"]["evalue"]
            # Getting the error's traceback into one single string
            traceback = ""
            for line in response["content"]["traceback"]:
                traceback += (line + '\n')
            cmd.stderr.traceback = traceback

        if is_new_cmd:
            self.cmd_history.append(cmd)

        return cmd


    def get_cmd_by_id(self, id):
        for cmd in reversed(self.cmd_history):
            if cmd.id == id:
                return cmd
        return None


    def show_history(self, history=None):
        if history == None:
            history = self.cmd_history

        for cmd in history:
            cmd.show_cmd()
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
        cmd_info = None

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
                    cmd_info = self.save_command_info(response)

                # We can stop listening to the kernel's responses if it
                # changes its status to 'idle' in response to OUR command.
                if response["content"]["execution_state"] == "idle" \
                    and self.is_response_to_self(response):
                    whole_response_received = True

            except: # Entered when there is no more reponses to get
                ...

        return cmd_info


    def run_python_script(self, filepath):
        self.run_python_command("%run " + str(filepath))


    def __del__(self):
        self.stop_channels()
