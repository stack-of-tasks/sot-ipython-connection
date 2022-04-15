import os
import sys

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from sot_kernel import SOTKernel


def main():
    kernel = SOTKernel()
    kernel.run()
    

if __name__ == "__main__" :
    main()