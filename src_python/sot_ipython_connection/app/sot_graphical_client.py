import sys
import os

from PyQt5 import QtWidgets

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from sot_client import SOTClient

def main(scripts_paths):
    ... # TODO: launch the qt client


if __name__ == "__main__":
    main()