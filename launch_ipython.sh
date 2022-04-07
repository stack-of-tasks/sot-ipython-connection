#!/bin/bash

#
# Executing lines at startup (successful):
#

#python -m IPython --InteractiveShellApp.exec_lines "abc = 2"


#
# Changing the .ipython directory to use init_lsst.py located in this directory:
#

#ipython_dir="$PWD""/.ipython/"

#export IPYTHONDIR=$ipython_dir
#python -m IPython

# Successful when setting TerminalIPythonApp.exec_lines:
#python -m IPython --ipython-dir=$ipython_dir 

#python -m IPython --ProfileDir.location=$ipython_dir


#
# Changing the profile directory to use init_lsst.py located in this directory:
#

#profile_dir="$PWD""/.ipython/profile_default/"
#python -m IPython --profile-dir=$profile_dir


#
# Using an extra config file:
#

#python -m IPython --config="./.ipython/profile_default/ipython_config.py"