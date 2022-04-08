# ipython_kernel_launcher

## Usage

#### Launching the kernel
```bash
python3 ./ipythonKernel.py
```

#### Launching a terminal-based client
```bash
jupyter console --existing
```
Warning: using `ipython` instead of `jupyter` will result in the `--existing` option being ignored and the client being launched with its own new kernel, in the same process.

#### Launching a Qt Console
```bash
ipython3 qtconsole --existing
```
Warning: using `jupyter` instead of `ipython` will result in errors at launch.

#### Connecting a client to a specific kernel
These last two commands will connect the clients to the latest kernel. To connect to a specific kernel, you can specify the name (or path) of its connection file (kernel-<number>.json) after `--existing`, as such:
```bash
jupyter console --existing kernel-73809.json
```

#### Configuring the kernel
You can also create .py or .ipy files in the IPython startup directory. These files will be run as IPython starts, in lexicographical order.
