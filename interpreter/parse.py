# This file takes aFex wordcode and converts it to aFex bytecode.
import re
import numpy as np

lgl_cmd = ['byteword', '=', 'for']

# Calculate indentation level of line
def indents(line):
    # Return a line with indentations removed, and return its indentation level
    # Example: extract_indentation([/t/t/thello, world]) == [hello, world], 3
    n = len(line[0]) - len(line[0].lstrip('\t'))
    line = [x.replace('\t', '') for x in line]
    return line, n

# Create the appropriate statements to end a for statement
def terminate_for(line, array, cindex, vardic, flagdic, flag_val, for_cap, debug=False, fill=False): # Declare variables and flags first
    print("Terminating for loop")
    # Vardic: array of arrays and their corresponding indexes in the byteword.
    # c index is the current farthest our commands are going
    # Generate an array of code that terminates the described for loop.
    # Should be like, '
    if not fill:
        code = [0] * 10 # move cursor 10 sport
    else:
        print(for_cap)
        flag_title = for_cap['flag']
        var_a = for_cap['incremental_var']
        var_b = for_cap['var_b']
        inc = for_cap['increment']
        op = {'==': 0, '!=': 1, '>=': 2, '>': 3, '<=': 4, '<': 5}[for_cap['op']]

        code = [1, 0, vardic[var_a], vardic[inc], vardic[var_a], 2, op, vardic[var_a], vardic[var_b], flagdic[flag_title] + 3] # Add
    if code[0] == 1:
        for c, nn in zip(code, range(len(code))):
            array[flag_val + nn] = c # Transcribe code snippet to the array
    #print("Encoded:", code, array)
    flag_val += len(code)



    return array, cindex, vardic, flagdic, flag_val

# Declare flags, for loops, and variables in memory before assembling commands.
def get_flags(line, array, cindex, vardic, flagdic, flag_val, active_for, flag_cnt, debug=False): # Declare variables and flags first
    # Vardic: array of arrays and their corresponding indexes in the byteword.
    # c index is the current farthest our commands are going
    # Active for: List of for loops we are actively in
    code = None
    if debug:
        print(flag_val, line)
    if line[0] == '=' : #Command for declaring flags and variables
        if line[2] == 'flag':
            flagdic[line[1]] = flag_val

        elif line[1] not in vardic:
            varindex = len(vardic) + 1

            varname = line[1]
            value = line[2]
            assert varname not in vardic, 'Variable with this name has been previously defined.'

            vardic[varname] = len(array) - varindex
            array[vardic[varname]] = value

        else:
            print("FIXME") # FIXME. We want to set variable values throughout the code.
            # Copy the value
            ...
    elif line[0] == 'for': # Add object to active_for
        flag_cnt += 1
        if len(line) == 5: # User has defined increment value
            # If it's not a variable, declare it as one (Only if it's a number).
            try:
                inc = float(line[4])
                # Add to the var dic
                if line[4] not in vardic:
                    varindex = len(vardic) + 1
                    varname = float(line[4])
                    value = float(line[4])
                    vardic[varname] = len(array) - varindex
                    array[vardic[varname]] = value
            except:
                inc = line[4]
        else:
            inc = 1
        title = 'for_{}_{}_{}_{}_{}'.format(line[1], line[2], line[3] , inc, flag_cnt)
        # Declare line[1:3] as variables (If it's not already)
        # line[1] set to a value of line[2]

        if line[1] not in vardic:
            varindex = len(vardic) + 1

            varname = line[1]
            value = line[2]
            vardic[varname] = len(array) - varindex
            array[vardic[varname]] = value
        for i in line[2:(len(line) - 1)]: # If floats are declared as boundaries,
            if i not in vardic:
                try:
                    float(i)
                    varindex = len(vardic) + 1
                    varname = i
                    value = float(i)
                    vardic[varname] = len(array) - varindex
                    array[vardic[varname]] = value
                except:
                    pass

        flagdic[title] = flag_val
        if inc >= 0: # What direction
            op = '>='
        else:
            op = '<='

        # Copy initializer value into incremental
        code = [0, 0, 0] # Transcribe to the array
        active_for.append({'flag': title, 'incremental_var': line[1], 'var_a': line[2], 'var_b': line[3], 'increment': inc, 'op': op, 'cnt': flag_cnt + 3}) # Add 3 because we add a copy operation before the flag



    # MATH FUNCTIONS
    if line[0] in ['^', '*', '/', '+', '-', 'flag']: # Functions with 5 arguments
        code = [0, 0, 0, 0, 0]
    elif line[0] == 'peek':
        code = [0, 0, 0, 0]
    elif line[0] == 'kill':
        code = [0]
    elif line[0] == '&': # Copy operator
        code = [0, 0, 0]
    if code is not None:
        flag_val += len(code)

    return array, cindex, vardic, flagdic, flag_val, active_for, flag_cnt

# Add commands to array.
def parse_array(line, array, cindex, vardic, flagdic, flag_val, active_for, flag_cnt, debug=False):
    # Vardic: array of arrays and their corresponding indexes in the byteword.
    # c index is the current farthest our commands are going
    code = None
    byteword = len(array)
    varindex = len(vardic) + 1
    if debug:
        print(flag_val, line)
    if line[0] == 'for':  # Add object to active_for
        flag_cnt += 1
        if len(line) == 5: # User has defined increment value

            inc = float(line[4])
        else:
            inc = 1
        title = 'for_{}_{}_{}_{}_{}'.format(line[1], line[2], line[3] , inc, flag_cnt)
        # Declare line[1:3] as variables (If it's not already)
        # line[1] set to a value of line[2]

        if line[1] not in vardic:
            varindex = len(vardic) + 1

            varname = line[1]
            value = line[2]
            vardic[varname] = len(array) - varindex
            array[vardic[varname]] = value
        for i in line[2:(len(line) - 1)]: # If floats are declared as boundaries,
            if i not in vardic:
                try:
                    float(i)
                    varindex = len(vardic) + 1
                    varname = i
                    value = float(i)
                    vardic[varname] = len(array) - varindex
                    array[vardic[varname]] = value
                except:
                    pass

        flagdic[title] = flag_val
        if inc >= 0: # What direction
            op = '>='
        else:
            op = '<='

        # Copy initializer value into incremental
        code = [0, vardic[line[2]], vardic[line[1]]] # Transcribe to the array
        active_for.append({'flag': title, 'incremental_var': line[1], 'var_a': line[2], 'var_b': line[3], 'increment': inc, 'op': op, 'cnt': flag_cnt + 3}) # Add 3 because we add a copy operation before the flag

   
    # MATH FUNCTIONS
    if line[0] in lgl_cmd:
        ...
    elif line[0] == '^': #Exponent function
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
        # flag [operator] [source asset] [source b] [False flag]
    
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
    else:
        print("Unknown command {}".format(line))
        exit()
    if code is not None:
        #print(code)
        for c, nn in zip(code, range(len(code))):
            array[flag_val + nn] = c # Transcribe code snippet to the array
        flag_val += len(code)

    return array, cindex, vardic, flagdic, flag_val, active_for, flag_cnt

# FIXME: Delete this part (Unnecessary)
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

# Strip line of comments
def decomment(line):
    # Remove any contents of asset line between (( )). Doesn't work for nested, IE '(( (( )) )). Only (( comment )) .
    firstC = False
    endC = False # True if the last character was asset )
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

# Convert a .rr file to bytecode
def compile(source, dest, debug=False):

    path = source
    word = []
    var_index = {}
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
    command_index = 1 #Location to jump to when we declare asset flag.
    indentation_level = 0
    active_for = [] # FILO list of for loops to satisfy
    flag_cnt = 0
    # This iteration assigns variables
    for set in word:# Iterate through the set to get the flags for pointer future
        prev_indentation_level = indentation_level

        #If the previous indentation level is higher, we need to end the for loops with comparator ops
        #We could make a list of for loops, with the last element the first for loop to finish
        #Number to satisfy equal to prev_indentation_level - indentation_level

        set, indentation_level = indents(set)
        for_loop_satisfy = prev_indentation_level - indentation_level
        if for_loop_satisfy > 0:
            # Iterate through active_for backwards.
            for satisfy_index in range(for_loop_satisfy):
                print("Active for: ", active_for)
                for_loop_cap = active_for[-1]
                active_for = active_for[:-1]
                # Add the comparison operations into the afex, and move cursor forward appropriately.
                # We will still need to add the relevent commands after this
                afex, cindex, var_index, flag_index, command_index = terminate_for(set, afex, cindex, var_index, flag_index,
                                                                               command_index, for_loop_cap, debug=debug)

        if debug:
            print("Flags: ", flag_index)
            print("Variable pointers: ", var_index)
        afex, cindex, var_index, flag_index, command_index, active_for, flag_cnt = get_flags(set, afex, cindex, var_index,
                                                                                             flag_index, command_index, active_for, flag_cnt, debug=debug)

    cindex = 1
    command_index = 1 #Location to jump to when we declare asset flag.
    indentation_level = 0
    active_for = [] # FILO list of for loops to satisfy
    flag_cnt = 0

    # This iteration assigns commands
    for set in word:
        prev_indentation_level = indentation_level

        #If the previous indentation level is higher, we need to end the for loops with comparator ops
        #We could make a list of for loops, with the last element the first for loop to finish
        #Number to satisfy equal to prev_indentation_level - indentation_level

        set, indentation_level = indents(set)
        for_loop_satisfy = prev_indentation_level - indentation_level

        if for_loop_satisfy > 0:
            # Iterate through active_for backwards.
            print(for_loop_satisfy, active_for)
            for satisfy_index in range(for_loop_satisfy):
                for_loop_cap = active_for[-1]
                active_for = active_for[:-1]
                # Add the comparison operations into the afex, and move cursor forward appropriately.
                # We will still need to add the relevent commands after this
                afex, cindex, var_index, flag_index, command_index = terminate_for(set, afex, cindex, var_index, flag_index,
                                                                               command_index, for_loop_cap, fill=True, debug=debug)

        afex, cindex, var_index, flag_index, command_index, active_for, flag_cnt = parse_array(set, afex, cindex, var_index, flag_index, command_index, active_for, flag_cnt, debug=debug)



    string = ''
    for x in afex:
        string += str(float(x)) + ' '
    if debug:
        print(string)
    #Write the string to dest file. 
    with open(dest, 'w') as d:
        d.write(string)
    print("Compiled {}".format(dest))
