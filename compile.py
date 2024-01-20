import argparse
import sys

from interpreter.parse import Compiler
import os

if __name__ == '__main__':
    compiler = Compiler()
    compiler.compile(src=sys.argv[1], dest=sys.argv[2], debug=True)



