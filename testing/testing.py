# River testing app
from os import listdir, walk, remove
import random
from os import popen

from interpreter import parse
import traceback, sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def run_test_by_name(name):
    src_path = f"../../testing/tests/{name}/code.rr"
    expected_out_path =  f"../../testing/tests/{name}/expected_out"

    # 1. Compile AFEX by source path
    print(f"Running test {name}. ")
    print("Compiling...")
    with open(src_path) as F:
        code = F.read()

    compiler = parse.Compiler()

    out = compiler.compile(code, mode='api')

    return_struc = {
        'error': False,
        'compiled': out['compiled'],
        'debug': out['debug']
    }
    try:
        pass

    except BaseException as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = ''
        stack_trace += "Exception type : %s <br> " % ex_type.__name__
        stack_trace += "Exception message : %s <br>" % ex_value
        for trace in trace_back:
            stack_trace+= "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3])

        print("ERROR")
        print(e)
        return_struc = {
            'error': True,
            'error_msg': stack_trace,
            'debug': compiler.debug_string
        }

        print("Stack trace : %s" % stack_trace)

    assert return_struc['error'] == False, "There was an error. "

    # Now at this point we have passed compilation, now run the compiled code and collect the output.

    src = f'../../testing/tmp_{random.randint(0, 999999)}' # Dump the bytes into some random file - we will clean it up after

    with open(src, 'w') as f:
        f.write(return_struc["compiled"])

    out = popen(f'bin/main {src}').read()
    return_struc = {
        'error': False,
        'resp': out
    }

    # Last stage - compare the real out with the expected out.

    # I expect this step to be finnicky because I'm just comparing raw strings, and I guess different CPUs might have different
    # idiosyncracies related to floating points and stuff. We may encouter issues related to this in the future which would
    # require a smarter approach but this is gonna be "quick and dirty" for my purposes today.

    with open(expected_out_path) as o:
        expected_out = o.read()

    print(bcolors.OKGREEN + "-- Expected out -- ")
    print(bcolors.OKBLUE + expected_out )
    print(bcolors.OKGREEN + "-- Actual out -- ")
    print(bcolors.OKBLUE + out)
    assert expected_out == out, bcolors.FAIL + 'expected output does not match!!!!!!!!!!'

    print(bcolors.OKGREEN + f"Hooray! Test {name} passed!" + bcolors.ENDC)

    remove(src)

def run_all_prestartup_checks():
    # Run all checks to validate the language is working properly.
    # Raise an exception if there's an issue.
    print(bcolors.OKBLUE + "Beginning Syntax Validation Checks!")
    print("Available tests: ", end=' ')
    test_list = []
    for (_, d, _) in walk("../../testing/tests"):
        print(d)
        if d != []:
            test_list= d
    print(test_list)
    for x in test_list:
        run_test_by_name(x)

    print(bcolors.ENDC)

