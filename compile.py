import argparse
from interpreter import parse
import os

if __name__ == '__main__':
    parse.compile(source='projects/arrays/arraytest.rr', dest='projects/arrays/arraytest.a', debug=True)
    input()
    os.system('./projects/arrays/arraytest.a')



