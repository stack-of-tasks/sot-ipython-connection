#!/bin/bash

#
# Executing lines at startup:
#

#python -m IPython kernel --InteractiveShellApp.exec_lines "c = 2"


#
# Changing the .ipython directory to use init_lsst.py located in this directory:
#

ipython_dir="$PWD""/.ipython/"

#export IPYTHONDIR=$ipython_dir
#python -m IPython kernel

jupyter console --ipython-dir=$ipython_dir

#python -m IPython kernel --ProfileDir.location=$ipython_dir


#
# Changing the profile directory to use init_lsst.py located in this directory:
#

#profile_dir="$PWD""/.ipython/profile_default/"
#python -m IPython kernel --profile-dir=$profile_dir

#
# Using an extra config file:
#

#python -m IPython kernel --config="./.ipython/profile_default/ipython_config.py"