from app import app
from flask import render_template, request, jsonify
import random
from os import popen


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

    parse.compile(src, dst)

    with open(dst) as f:
        out = f.readlines()
    print(out)
    return_struc = {
        'error': False,
        'compiled': out
    }

    return jsonify(return_struc)

@app.route("/")
def index():
    return render_template("base.html")