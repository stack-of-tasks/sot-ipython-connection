# sot_ipython_connection

The purpose of this package is to implement a flexible connection between the Stack of Tasks and a client controlling it.
sot-ipython-connection makes the entire python language available to the user in order to communicate with the SoT.

### Install
TODO

### Overview
sot-ipython-connection has two main parts: SOTKernel and SOTClient, which are based on the ipython kernel and client and implement functionalities specific to the use of the SoT.

The kernel is a python interpreter which will be running on the robot processor, and which will contain the SoT. One or several clients can be run on separate computers, to allow users to handle the robot.


### Executables
Two executables are made available in this package: sot-interpreter and sot-script-executer.

#### sot_interpreter
This is the kernel to run on the robot’s processor. To launch it, use the following command:

`python3 ./sot_interpreter`

![](https://github.com/justinefricou/sot-ipython-connection/blob/main/doc/img/kernel.png)

Figure 1: sot-interpreter running

To interact with it, you have to use a client.
To launch a terminal-based client that will connect with this kernel, use the following command, after launching the kernel:

`jupyter console --existing`

The --existing option means that the client will connect to the latest running kernel. In the case of sot_interpreter, there can be only one running at a time on the same computer, as several sot_interpreters would use the same ports.

![](https://github.com/justinefricou/sot-ipython-connection/blob/main/doc/img/client.png)

Figure 2: Example of interactions with a jupyter console

#### sot_script_executer
This is a client that allows the user to execute python scripts on the kernel:

`python3 ./sot_script_executer pathToScript1 [pathToScript2] [--local]`

If you wish to execute several scripts, add them to the command in the order you want them to be executed. For instance, in the above command, script1 will be executed before script2.

Use the –local option if the scripts to execute are located on the same machine as the client. Otherwise, they will be considered to be on the same machine as the kernel.
