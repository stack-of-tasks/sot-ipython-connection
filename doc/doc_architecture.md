# Architecture

### SOTKernel
The SOTKernel class contains an ipython kernel which can be configured and run.
There are two ways to launch it:
- A blocking call (with its method run). In this case, the kernel can be stopped by entering the command ‘quit’ in a terminal-based client.
- A non-blocking call (with its method run_non_blocking), which calls the run method in a subprocess. In this case, the subprocess is stopped in the __del__ method and the kernel is stopped automatically.

In connection_config.py, you can configure the connection between the client and the kernel, including the ports. As this file is part of the package, a new build is needed after it has been modified.
To know more about the kernel-client communication, visit [this link](https://jupyter-client.readthedocs.io/en/latest/messaging.html#messaging-in-jupyter).

![](https://github.com/justinefricou/sot-ipython-connection/blob/main/doc/img/connection-config.png)

Figure 1: Example of content for the connection configuration file

In kernel_namespace_config.py, you can configure the initial namespace for the kernel, i.e the list of variables that will be automatically added to the kernel at launch. For this file too, because it is part of the package, a new build is needed after it has been modified.

![](https://github.com/justinefricou/sot-ipython-connection/blob/main/doc/img/namespace.png)

Figure 2: Example of content for the kernel namespace configuration file


### SOTClient
The SOTClient class can launch and stop instances of ipython clients (BlockingKernelClient) that automatically connect to the latest running kernel.

#### How to connect to a SOTKernel
SOTClient stores a running client instead of inheriting BlockingKernelClient in order to be able to stop and relaunch the client without needing to instantiate a new SOTClient object.

After creating a SOTClient object, call the connect_to_kernel method to launch the client. The client will be stopped in the __del__ method.

If the kernel was stopped and a new kernel instance has been launched, to connect the SOTClient to this new kernel, call the connect_to_kernel method again. This stops the running client (if any) and launches a new one, connected to the new kernel.

Therefore, there cannot be more than one instance of an ipython client running in a SOTClient, but there can be multiple SOTClient running at the same time.

The is_kernel_alive method allows to know if the kernel is still running.
Warning: because all SOTKernels use the same ports (because of the connection configuration file), if a client is kept running while the kernel is stopped and a new kernel is relaunched, is_kernel_alive will start returning True again once this new kernel is launched, while the client will consider to still be connected to the old kernel.

SOTClient will send commands on the right ports, but will communicate using the wrong kernel session id. This will cause a crash on both the kernel and the client.
To prevent this, when is_kernel_alive returns False (kernel was stopped) and then True (a new kernel was launched), call connect_to_kernel to connect to the new kernel.

#### How to run commands on the kernel
The run_python_command method takes a string containing a python command, sends it to the kernel, and reads its response. It returns a SOTCommandInfo object containing information on the command. This object is then added to the client’s command history (see the dedicated section for more details).

The run_local_python_script and run_kernel_side_python_script methods allow to execute entire scripts on the kernel, depending on their location (client-side or kernel-side).


#### The command history
Each command sent by the client to the kernel is stored into the command history, alongside the kernel response.

When sending a command, the kernel response is divided into several parts, described on [this web page](https://jupyter-client.readthedocs.io/en/latest/messaging.html#messaging-in-jupyter).
For each part of the response received, SOTClient adds the information it contains (if any) to a SOTCommandInfo object thanks to the _save_response method. For instance:
- 1st part of the response: the kernel answer is ‘busy’ to indicate it is starting to work on this command  -> the SOTCommandInfo object is created.
- 2nd part of the response: the type of the answer is ‘execute_input’, i.e it contains the content of the command -> this content is added to the SOTCommandInfo object. It is added during this step rather than when sending the command to the kernel, because this will allow to store any other client’s command using this method in the future.
- 3rd part of the response: the type of answer is ‘execute_result’, i.e it contains the result of the command -> the result is added to the SOTCommandInfo object.
- 4th part of the response: the kernel answer is ‘idle’ to indicate it has finished working on this command  -> we stop reading the kernel responses.

The errors are stored as SOTCommandError instances. They contain the name, value and traceback of the error, as sent by the kernel.

The print_history method allows to print a command history. It can work with any history, i.e the history of the client calling this method, another client’s, or all clients. This will be useful in the future, when the possibility of storing other client histories is added.

![](https://github.com/justinefricou/sot-ipython-connection/blob/main/doc/img/history.png)

Figure 3: Example of a past command in the command history

### Tests
Pytest is used for the functional tests.
There is a test class for each feature, and all of these inherit BaseTestClass, which, for each test method, launches a non-blocking kernel, executes the test, and stops the kernel.
