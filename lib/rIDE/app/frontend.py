from app import app
from flask import render_template, request, jsonify
import random
import sys
from os import popen
import traceback

from interpreter import parse


@app.route("/run", methods=['POST', 'GET'])
def run():

    tkn = random.randint(100000, 999999999999)
    bytes = request.args.get('bytes', '', str)
    print(bytes)
    src = 'tmp/' + str(tkn) + '_src'
    print(src)
    with open(src, 'w') as f:
        f.write(bytes)
    out = popen(f'bin/main {src}').read()
    print(out)
    return_struc = {
        'error': False,
        'resp': out
    }


    return return_struc


@app.route("/compile", methods=['POST', 'GET'])
def compile():
    tkn = random.randint(100000, 999999999999)
    code = request.args.get('code', '', str)
    src = 'tmp/' + str(tkn) + '_src'
    dst = 'tmp/' + str(tkn) + '_dst'

    with open(src, 'w') as f:
        f.write(code)
    # parse.compile(src, dst)
    try:
        parse.compile(src, dst)
        with open(dst) as f:
            out = f.readlines()
        print(out)
        return_struc = {
            'error': False,
            'compiled': out
        }
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
            'error_msg': stack_trace
        }

        print("Stack trace : %s" % stack_trace)
    return jsonify(return_struc)

@app.route("/")
def index():
    return render_template("base.html")