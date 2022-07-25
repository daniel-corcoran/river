import argparse
import sys

from interpreter import parse
import os

if __name__ == '__main__':
    parse.compile(path=sys.argv[1], dest=sys.argv[2], debug=False)



