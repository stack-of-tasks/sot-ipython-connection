from typing import Any, Dict, List, Union
from pathlib import Path

from time import sleep
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


def get_latest_connection_file_path() -> Union[str, None]:
    """ Returns the path of the most recent jupyter kernel connection file, or
        `None` is none was found.
    """
    directory_path = Path(jupyter_core.paths.jupyter_runtime_dir())
    connection_files = directory_path.glob("*")
    if connection_files == []:
        return None
    return max(connection_files, key=lambda x: x.stat().st_ctime)


class SOTCommandError:
    """ Represents an error sent by the kernel in response to a client's
        command.

        Public methods:
        - `traceback()`: returns the exception's formatted traceback.
        - `name()`: returns the exception's name.
        - `value()`: returns the exception's value.
    """

    def __init__(self):
        self._traceback: str = None
        self._name: str = None
        self._value: str = None


    def __str__(self):
        return self.traceback
    def __repr__(self):
        return f"_name: {self._name}\n_value: {self._value}\n\
                _traceback: {self._traceback}\n"


    def traceback(self) -> str:
        return self._traceback
    def name(self) -> str:
        return self._name
    def value(self) -> str:
        return self._value


class SOTCommandInfo:
    """ Represents a command and its information.

    Public attributes:
        - `id` (`str`): id of the request containing the command.
        - `session_id` (`str`): id of the client session that sent the request.
        - `content` (`str`): content of the command.
        - `result` (`Any`, optional): result sent by the kernel if the request
          was of the `execute_input` type (e.g '2+2'). If the kernel's result is not
          parsable by `eval()`, it will be stored unparsed.
        - `stdout` (`str`, optional): output sent by the kernel if its response was of
          the `stream` type (e.g a response to the command "print('hello')" which
          has a type `execute_request`).
        - `stderr` (`SOTCommandError`, optional): error sent by the kernel in response
          to this command.
    """

    def __init__(self, id: str, session_id: str):
        self.session_id = session_id
        self.id = id
        self.content: str = None
        self.result: Any = None
        self.stdout: str = None
        self.stderr: SOTCommandError = None


    def __str__(self):
        string = ""
        string += f"Session id: {self.session_id}\n"
        string += f"Command id: {self.id}\n"
        string += f"Command: {self.content}\n"
        if self.result:
            string += f"Result: {self.result} ({type(self.result)})\n"
        if self.stdout:
            string += f"Output: `{self.stdout}`\n"
        if self.stderr:
            string += f"Error output: {self.stderr.traceback}\n"
        return string


    def __repr__(self):
        string = ""
        string += f"session_id: {self.session_id}\n"
        string += f"id: {self.id}\n"
        string += f"content: {self.content}\n"
        if self.result:
            string += f"result: {self.result} ({type(self.result)})\n"
        if self.stdout:
            string += f"stdout: `{self.stdout}`\n"
        if self.stderr:
            string += "stderr:\n"
            repr(self.stderr)
        return string


class SOTClient():
    """ An ipython client with blocking APIs to communicate with a SOTKernel.

        Public attributes:
        - `session_id` (`str`): the client's current session id. If the client
          has to be relaunched, this id will change. It can be used to
          differentiate the current session's commands from the others sessions'
          (e.g in the command history).
        - `cmd_history` (`[SOTCommandInfo]`): a history of the current session's
          commands (in the future, it would be great to store every session's commands).
    """
    
    def __init__(self):
        # We have to store an instance of BlockingKernelClient as an attribute instead
        # of inheriting from it, because the channels of a client cannot be started twice,
        # even after stopping them:
        # https://ipython.org/ipython-doc/3/api/generated/IPython.kernel.client.html
        # Inheriting would mean having to create a new SOTClient at every reconnection.
        self._client: BlockingKernelClient = None
        self.session_id: str = None

        self.cmd_history: List[SOTCommandInfo] = []
        # TODO: the get_iopub_msg() call used in run_python_command returns responses to
        # every client (session) connected to the kernel.
        # To store a history of every session's commands, we should listen to the kernel's
        # iopub channel in another thread and save the commands with the method currently 
        # used, as self._save_response() already saves the command's session id (which
        # allows to differentiate every client)
        # self.get_self_history currently has no use, as self.cmd_history only store this
        # session's commands.

        self.connect_to_kernel()
        

    def __del__(self):
        self._stop_client()


    def is_kernel_alive(self) -> bool:
        """ Returns `True` if activity is detected on the heartbeat of the
            kernel this session is connected to.
        """
        return self._client.is_alive()
        

    # FIXME: if a new SOTKernel is launched but the connection is not reset
    # (= new instance of BlockingKernelClient), the kernel and the client will
    # be unusable (reproducible by launching sot_interpreter and a jupyter console)
    def connect_to_kernel(self) -> bool:
        """ Creates a client and connects it to the latest kernel.
            `True` is returned if a connection could be established, `False` if not.
            If a client is already running, it will be stopped and replaced.
        """
        # Stopping the already running client if needed:
        self._stop_client()

        # Creating an instance of a client:
        self._client = BlockingKernelClient()
        self.session_id = self._client.session.session

        # Getting the latest kernel's connection file:
        connection_file_path = get_latest_connection_file_path()
        if connection_file_path is None:
            print("SOTClient.connect_to_kernel: connection failed (no connection file found)")
            return False

        # Connecting to the kernel:
        self._client.load_connection_file(connection_file_path)
        self._client.start_channels()

        # We have to wait for the channels to finish opening before testing the
        # connection or the kernel will appear as alive even if it's not:
        sleep(1)
        try:
            self.check_connection()
        except ConnectionError:
            print('SOTClient.connect_to_kernel: connection failed (kernel is not alive).')
            return False
        
        return True


    def _stop_client(self) -> None:
        """ Stop the running client, if any. """
        if self._client is not None:
            if self._client.channels_running:
                self._client.stop_channels()
            self._client = None


    def check_connection(self) -> None:
        """ Waits up to 2s for the connection to the kernel to complete, and raises
            a ConnectionError if it doesn't.
        """
        # Waiting for the connection to finish if it's new:
        for _ in range(5):
            if self.is_kernel_alive():
                break
            sleep(0.1)

        # It the connection is still not working:
        if not self.is_kernel_alive():
            raise ConnectionError('No connection to kernel')


    def run_python_command(self, cmd: str) -> SOTCommandInfo:
        """ This is a blocking function that sends a command to the kernel and 
            waits for it to respond completely (see link to the doc on messaging
            with jupyter for every step), while saving each response into a new
            instance of `SOTCommandInfo` in the command history.
            It then returns this new instance.
            Raises a `ConnectionError` if there is no connection to the kernel.

            Arguments:
            - `cmd`: the command to be sent to the kernel
        """
        if self._client is None:
            raise ValueError('self._client is None: cannot send command to kernel.')

        # Checking if the connection to the kernel is ready / still open
        self.check_connection()

        # Sending the command to the kernel
        msg_id = self._client.execute(cmd)
        cmd_info = None

        whole_response_received = False
        while not whole_response_received:
            try:
                # iopub is the channel where the kernel broadcasts side-effects
                # (stderr, stdout, debugging events, its status: busy or idle, etc)
                # to every client connected to it
                response = self._client.get_iopub_msg()

                # Saving the response to the command history only if it responds
                # to our command
                if response["parent_header"]["msg_id"] == msg_id:
                    cmd_info = self._save_response(response)

                # We can stop listening to the kernel's responses if it
                # changes its status to 'idle' in response to our command.
                if response["content"]["execution_state"] == "idle" \
                    and self._is_response_to_self(response):
                    whole_response_received = True

            except: # Entered when there was no response to read yet
                ...

        return cmd_info


    def run_local_python_script(self, filepath: str) -> None:
        """ Runs a python script on the kernel.

            Arguments:
            - `filepath`: the script's path. It must be either absolute
            (on the same machine as the client), or relative to the
            directory from which the client was launched
        """
        if Path(filepath).exists():
            with open(filepath, 'r') as file:
                file_content = file.read()
            self.run_python_command(file_content)
        else:
            print("Could not execute script: file " + filepath + " does not exist.")


    def run_kernel_side_python_script(self, filepath: str) -> None:
        """ Runs a python script on the kernel.

            Arguments:
            - `filepath`: the script's path. It must be either absolute
            (on the same machine as the kernel), or relative to the directory
            from which the kernel was launched
        """
        self.run_python_command("%run " + str(filepath))


    def _is_response_to_self(self, response: Dict) -> bool:
        """ Returns True if the `response` argument is a response to a request
            sent by the current client session.

            Arguments:
            - `response`: the response as sent by the kernel
        """
        return self.session_id == response["parent_header"]["session"]


    def _save_response(self, response: Dict) -> SOTCommandInfo:
        """ Saves the `response`'s information as a `SOTCommandInfo`'s
            attribute in the command history and returns the created or modified
            `SOTCommandInfo` instance.
            Each response contains the `SOTCommandInfo`'s `session_id` and `id`,
            in addition to either `content`, `result`, `stdout` or `stderr`. Hence,
            several calls to this function are necessary to fully store a command's
            information.

            Arguments:
            - `response`: the response as sent by the kernel
        """

        # Trying to find a command in the history with the same id as `response`
        cmd = self._get_cmd_by_id(response["parent_header"]["msg_id"])
        is_new_cmd = False

        # Creating the command if this is its first response
        if cmd == None:
            is_new_cmd = True
            session_id = response["parent_header"]["session"]
            id = response["parent_header"]["msg_id"]
            cmd = SOTCommandInfo(id, session_id)
        
        # Saving the command's content
        if response["msg_type"] == "execute_input":
            cmd.content = response["content"]["code"]

        # Saving the command's result
        if response["msg_type"] == "execute_result":
            try:
                # Trying to parse the response
                cmd.result = eval(response["content"]["data"]["text/plain"])
            except:
                # If the data is not parsable (e.g if it's a type), we store the string
                cmd.result = response["content"]["data"]["text/plain"]

        # Saving the command's stdout
        if response["msg_type"] == "stream":
            cmd.stdout = response["content"]["text"]

        # Saving the command's error
        if response["msg_type"] == "error":
            cmd.stderr = SOTCommandError()
            cmd.stderr.name = response["content"]["ename"]
            cmd.stderr.value = response["content"]["evalue"]
            cmd.stderr.traceback = '\n'.join(response["content"]["traceback"])

        # Adding the command to the history if this is its first response
        if is_new_cmd:
            self.cmd_history.append(cmd)

        return cmd


    def _get_cmd_by_id(self, id: str) -> Union[SOTCommandInfo, None]:
        """ Looks for the command in the history and returns it if it was
            found. Else, returns None.

            Arguments:
            - `id`:  id of the client's request containing the command
        """

        # We search from newest to oldest:
        for cmd in reversed(self.cmd_history):
            if cmd.id == id:
                return cmd
        return None


    def print_history(self, history: List[SOTCommandInfo] = None) -> None:
        """ Prints the infomation of each command of `history`,
            which defaults to `self.cmd_history`.
        """
        if history == None:
            history = self.cmd_history

        for cmd in history:
            print(str(cmd) + '\n')


    def print_self_history(self) -> None:
        """ Prints the information of each command sent by the current session. """
        self_history = self.get_self_history()
        self.print_history(self_history)


    def get_self_history(self) -> List[SOTCommandInfo]:
        """ Returns a filtered copy of the command history by keeping
            only the commands that were sent by the current session.
        """
        self_history = []
        for cmd in self.cmd_history:
            if cmd.session_id == self.session_id:
                self_history.append(cmd)
        return self_history
