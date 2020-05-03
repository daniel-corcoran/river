import argparse
from interpreter import parse
import os

if __name__ == '__main__':
    parse.compile(source='projects/for_loops/nested_for.rr', dest='projects/for_loops/nested_for.a', debug=True)
    input()
    os.system('./river projects/for_loops/nested_for.a')



