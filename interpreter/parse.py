# This file takes aFex wordcode and converts it to aFex bytecode.
import re
import numpy as np


def parse2_array(line, array, cindex, vardic, flagdic, flag_val):
    # Vardic: array of arrays and their corresponding indexes in the byteword.
    # c index is the current farthest our commands are going
    byteword = len(array)
    varindex = len(vardic) + 1
    print(flag_val, line)
    if line[0] == 'declare': #Command for declaring flags and variables

        if line[2] == 'flag':
            #print("Flag at", flag_val)
            flagdic[line[1]] = flag_val #FIXME: command index the interpreter jumps to during the process

        else:
            varname = line[1]
            value = line[2]
            #print("We need to declare a variable ", varname, 'value', value)
            assert varname not in vardic, 'Variable with this name has been previously defined.'
            vardic[varname] = len(array) - varindex
            array[vardic[varname]] = value
    
   
    code = None
    # MATH FUNCTIONS
    if line[0] == '^': #Exponent function
        source_a = line[1]
        source_b = line[2]
        dest = line[3]
        #print("{}^{} -> {}".format(source_a, source_b, dest))
        # 1 4 sa sb d
        code = [1, 4, vardic[source_a], vardic[source_b], vardic[dest]]
    elif line[0] == '*': # Multiply function
        source_a = line[1]
        source_b = line[2]
        dest = line[3]
        #print("{}*{} -> {}".format(source_a, source_b, dest))
        #1 2 sa sb d
        code = [1, 2, vardic[source_a], vardic[source_b], vardic[dest]]
    elif line[0] == '/': #Divide function
        source_a = line[1]
        source_b = line[2]
        dest = line[3]
        #print("{}/{} -> {}".format(source_a, source_b, dest))
        #1 3 sa sb d
        code = [1, 3, vardic[source_a], vardic[source_b], vardic[dest]]
    elif line[0] == '+': #Add function
        source_a = line[1]
        source_b = line[2]
        dest = line[3]
        #print("{}+{} -> {}".format(source_a, source_b, dest))
        #1 0 sa sb d
        code = [1, 0, vardic[source_a], vardic[source_b], vardic[dest]]
    elif line[0] == '-': #minus function
        source_a = line[1]
        source_b = line[2]
        dest = line[3]
        #print("{}-{} -> {}".format(source_a, source_b, dest))
        #1 1 sa sb d
        code = [1, 1, vardic[source_a], vardic[source_b], vardic[dest]]
    elif line[0] == 'flag': # Flag function. 
        # flag [operator] [source a] [source b] [False flag]
    
        operator =  {'==': 0, '!=': 1, '>=': 2, '>': 3, '<=': 4, '<': 5}[line[1]]
        source_a = line[2]
        source_b = line[3]
        false_flag = line[4]
        # If the statement source_a [operator] source_b is true, continue else go to false_flag
        code = [2, operator, vardic[source_a], vardic[source_b], flagdic[false_flag]]
    elif line[0] == 'peek':
        source = line[1]
        code = [0, vardic[source], 0, 4]
    elif line[0] == 'kill':
        code = [5]
    elif line[0] == '&': # Copy operator
        src = line[1]
        dst = line[2]
        code = [0, vardic[src], vardic[dst]]

    if code is not None:
        #print(code)
        for c, nn in zip(code, range(len(code))):
            array[flag_val + nn] = c # Transcribe code snippet to the array
        flag_val += len(code) 




    return array, cindex, vardic, flagdic, flag_val

def get_byteword(word):
    byteword_exists = False # Has the user declared the program byteword
    for operation in word:
        if 'byteword' in operation:
            byteword = operation[1]
            byteword_exists = True
    assert byteword_exists, 'ERROR. no byteword declared, program cannot compile. '
    assert int(byteword) == float(byteword), 'ERROR. byteword must be of type int'
    byteword = int(byteword)
    assert byteword > 1, 'Program must be at least one byteword.'
    print("BYTEWORD:", byteword)
    return byteword


def decomment(line):
    # Remove any contents of a line between (( )). Doesn't work for nested, IE '(( (( )) )). Only (( comment )) .
    firstC = False
    endC = False # True if the last character was a )
    ignore = False
    newstr = ''
    for x in line:
        #If we have two successive (, start ignoring.
        # if we have two successive ), stop ignoring.
        if x == ')':
            ignore = endC
            endC =not True
        else:
            endC = False
        if x == '(':
            ignore = firstC
            firstC = True
        else:
            firstC = False
        if ignore:
            pass
        elif (x != '(' and not firstC) and (x != ')' and not endC):
            newstr += x
    return newstr

def compile(source, dest):
    path = source
    word = []
    var_index = {}
    byteword = 0
    flag_index = {}

    file = open(path)
    for line in file:
        word_line = decomment(line)
        specific_lines = word_line.split(';')
        for sl in specific_lines:
            if sl not in ['', '\n']:
                operation = []
                sl = sl.split(' ')
                for key in sl:
                    if key not in ['', '\t', '\n']:
                        key = re.sub('\n', '', key)
                        if len(key) > 0:
                            operation.append(key)
                if len(operation) > 0:
                    word.append(operation)


    byteword = get_byteword(word)
    afex = np.zeros(byteword)
    cindex = 1
    command_index = 1 #Location to jump to when we declare a flag. 
    for set in word:
        afex, cindex, var_index, flag_index, command_index = parse2_array(set, afex, cindex, var_index, flag_index, command_index)
    print("Flags: ", flag_index)
    print("Variable pointers: ", var_index)
    string = ''
    for x in afex:
        string += str(int(x)) + ' '
    print(string)
    #Write the string to dest file. 
    with open(dest, 'w') as d:
        d.write(string)


    # First things first, we need to get the size of the overall array.




compile(source='projects/fibonacci_sequence.afex', dest='fib_seq.a')
