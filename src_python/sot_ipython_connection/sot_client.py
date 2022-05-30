from os.path import exists
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
    """ Returns the path of the most recent jupyter kernel connection file 
    """
    # TODO: better error management if there is no file
    directory_path = Path(jupyter_core.paths.jupyter_runtime_dir())
    connection_files = directory_path.glob("*")
    assert connection_files != []
    return max(connection_files, key=lambda x: x.stat().st_ctime)


class SOTCommandInfo:
    """ Represents a command and its information:
        - self.id (str):
          The id of the request containing the command.
        - self.session_id (str):
          The id of the client session that sent the request.
        - self.content (str):
          The content of the command.
        - self.result (any type, optional):
          The result sent by the kernel if the request was of the `execute_input`
          type (e.g '2+2'). If the kernel's result is not parsable by `eval()`,
          it will be stored unparsed.
        - self.stdout (str, optional):
          The output sent by the kernel if its response was of the `stream` type
          (e.g a response to the command "print('hello')" which has a type
          `execute_request`).
        - self.stderr (SOTCommandError, optional):
          The error sent by the kernel in response to this command.
    """

    class SOTCommandError:
        """ Represents an error sent by the kernel in response to a client's
            command:
            - self.traceback (str): The exception's formatted traceback.
            - self.name (str): The exception's name.
            - self.value (str): The exception's value.
        """
        def __init__(self):
            self.traceback = None
            self.name = None
            self.value = None


        def __repr__(self):
            return self.traceback


    def __init__(self):
        self.session_id = None
        self.id = None
        self.content = None
        self.result = None
        self.stdout = None
        self.stderr = None


    def print_cmd(self):
        """ Prints the command's information. """

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
    """ (Inherits BlockingKernelClient)
        An ipython client with blocking APIs to communicate with a SOTKernel.
        - self.session_id (str): the client's current session id. If the client
          has to be relaunched, this id will change. It can be used to
          differentiate the current session's commands from the others sessions'
          (e.g in the command history).
        - self.cmd_history ([SOTCommandInfo]): a history of the current session's
          commands (in the future, it would be great to store every session's commands).
    """
    
    def __init__(self):
        self.session_id = self.session.session
        self.cmd_history = []
        """ TODO: the get_iopub_msg() call used in this program returns responses to
            every client (session) connected to the kernel.
            To store a history of every session's commands, we should listen to the kernel's
            iopub channel in another thread and save the commands with the method currently 
            used, as self.save_response() already saves the command's session id (which
            allows to differentiate every client)
            self.get_self_history currently has no use, as self.cmd_history only store this
            session's commands.
        """

        # Setting up and starting the communication with the kernel
        self.load_connection_file(get_latest_connection_file_path())
        self.start_channels()
        

    def __del__(self):
        self.stop_channels()


    def is_kernel_alive(self):
        """ Returns True if activity is detected on the heartbeat of the
            kernel this session is connected to.
        """
        raise NotImplementedError
        # TODO: listen to the kernel's heartbeat on the hb channel


    def reconnect_to_kernel(self):
        """ Reconnects this client to the latest kernel """
        raise NotImplementedError
        # TODO


    def is_response_to_self(self, response):
        """ Returns True if the `response` argument is a response to a request
            sent by the current client session.
        """
        if self.session_id == response["parent_header"]["session"]:
            return True


    def save_response(self, response):
        """ Saves the `response`'s information as part of a `SOTCommandInfo`'s
            attributes in `self.cmd_history` and returns the created or modified
            `SOTCommandInfo`.
            Each response contains the `SOTCommandInfo`'s `session_id` and `id`,
            in addition to either `content`, `result`, `stdout` or `stderr`. Hence,
            several calls to this function are necessary to fully store a command's
            information.
            - response (dict): the response as sent by the kernel
        """
        # Creating the command if this is its first response
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
                # If the data is not parsable (e.g if it's a type), we store
                # the string
                cmd.result = response["content"]["data"]["text/plain"]

        # Saving the command's stdout
        if response["msg_type"] == "stream":
            cmd.stdout = response["content"]["text"]

        # Saving the command's error
        if response["msg_type"] == "error":
            cmd.stderr = cmd.SOTCommandError()
            cmd.stderr.name = response["content"]["ename"]
            cmd.stderr.value = response["content"]["evalue"]
            cmd.stderr.traceback = '\n'.join(response["content"]["traceback"])

        # Adding the command to the history if this is its first response
        if is_new_cmd:
            self.cmd_history.append(cmd)

        return cmd


    def get_cmd_by_id(self, id):
        """ Looks for the command in the history and returns it if it was
            found. Else, returns None.
            - id (str): the id of the client's request containing the command
        """
        for cmd in reversed(self.cmd_history):
            if cmd.id == id:
                return cmd
        return None


    def print_history(self, history=None):
        """ Prints the infomation of each command of `history`,
            which defaults to `self.cmd_history`.
        """
        if history == None:
            history = self.cmd_history

        for cmd in history:
            cmd.print_cmd()
            print()


    def print_self_history(self):
        """ Prints the infomation of each command of `self.cmd_history`.
        """
        self_history = self.get_self_history()
        self.print_history(self_history)


    def get_self_history(self):
        """ Returns a filtered copy of self.cmd_history by keeping
            only the commands that were sent by the current session.
        """
        self_history = []
        for cmd in self.cmd_history:
            if cmd.session_id == self.session_id:
                self_history.append(cmd)


    def run_python_command(self, cmd):
        """ This is a blocking function that sends a command to the kernel and 
            waits for it to respond completely (see link to the doc on messaging
            with jupyter for every step), while saving each response into a new
            instance of SOTCommandInfo in self.cmd_history. Returns this new instance.
            - cmd (str): the command to be sent to the kernel
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
                    cmd_info = self.save_response(response)

                # We can stop listening to the kernel's responses if it
                # changes its status to 'idle' in response to our command.
                if response["content"]["execution_state"] == "idle" \
                    and self.is_response_to_self(response):
                    whole_response_received = True

            except: # Entered when there is no more reponses to get
                ...

        return cmd_info


    def run_local_python_script(self, filepath):
        """ Runs a python script on the kernel.
            - filepath (str): the script's path. It must be either absolute
            (on the same machine as the client), or relative to the
            directory from which the client was launched
        """
        if exists(filepath):
            with open(filepath, 'r') as file:
                file_content = file.read()
            self.run_python_command(file_content)
        else:
            print("Could not execute script: file " + filepath + " does not exist.")


    def run_kernel_side_python_script(self, filepath):
        """ Runs a python script on the kernel.
            - filepath (str): the script's path. It must be either absolute
            (on the same machine as the kernel), or relative to the directory
            from which the kernel was launched
        """
        self.run_python_command("%run " + str(filepath))
