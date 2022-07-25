# This file takes aFex wordcode and converts it to aFex bytecode.
import re
import numpy as np
import itertools
from interpreter.decompose_0_0_2b import dec, split_commands_and_args, pretty_print_command_tree, mathop


def decompile(code, var_dic):
    # Prettily prints compiled code so we can validate it.

    print("_________________")
    print("afex generated")
    print("\n\n\n\n")

    for line in code:
        print(line)
        solved = False
        command = int(line[0])

        if (len(line) > 1):
            args = line[1:]

            if command == 0:
                solved = True
                print("COPY", args[0], 'TO', args[1])
            elif command == 1:
                solved = True

                print("MATHCHAIN", args)
            elif command == 2:
                solved = True

                print("COMPARE", args)
            elif command == 3:
                solved = True

                print("GOTO", args)
            elif command == 4:
                solved = True

                print("PRINT", args)
        else:
            if command == 5:
                solved = True

                print("TERMINATE")
            # Single op command with no args
        if not solved:
            print("ERROR CANNOT SOLVE")
            print(line)
            input()


# Calculate indentation level of line
def indents(line):
    # Return a line with indentations removed, and return its indentation level
    # Example: extract_indentation([/t/t/thello, world]) == [hello, world], 3
    n = len(line[0]) - len(line[0].lstrip('\t'))
    line = [x.replace('\t', '') for x in line]
    return line, n


# Declare all legal flag variables. Replace with program indexes before variable interpolation
def grab_flags(word, flag_dic):
    # Returns a dictionary of flags that are legal jump points
    for line in word:
        if line[0] == 'flag':
            # Add to the flag dic
            flag_dic[line[1]] = len(flag_dic)
    return flag_dic


# Create the appropriate statements to end a for statement
def terminate_for(code, for_loop_cap, var_dic):  # Declare variables and flags first
    print("Terminating for loop")
    print(for_loop_cap)

    flag_title = for_loop_cap['flag']
    initializer = for_loop_cap['initializer']
    incremental = for_loop_cap['incremental']
    conditional = for_loop_cap['conditional']
    print(conditional)
    goto_point = for_loop_cap['goto_point']
    assert len(conditional) == 3

    op = {'==': 0, '!=': 1, '>=': 2, '>': 3, '<=': 4, '<': 5}
    reverse_op = {'==': 1, '!=': 0, '>=': 4, '>': 5, '<=': 2, '<': 3}
    # TODO: Construct termination string.
    out = [2,
           reverse_op[conditional[0]],
           '*{}'.format(conditional[1]),
           '*{}'.format(conditional[2]),
           goto_point]
    print(out)

    code += [incremental, out]


    # Afex continues if true, otherwise it returns to the goto index
    # 2 operatorcode index_a index_b goto_index

    # We will actually have to reverse the polarity of the conditional for this...



    return code, var_dic


def process_equal(line, var_dic, debug=False):

    print(line)
    print(var_dic)
    # = Follows the format [dst, src]
    try:
        float(line[2])
        if line[2] not in var_dic:
            var_dic[line[2]] = len(var_dic)
        # line[2] is the floating point value we need to declare and copy to the line[1] pointer
        if line[1] not in var_dic:
            var_dic[line[1]] = len(var_dic)
        # 0 src dest
        transcribe = ['0', '*{}'.format(line[2]), '*{}'.format(line[1])]
        print("A")

    except:  # input is not a float..
        if line[2] in var_dic:
            print("B")

            if line[1] not in var_dic:
                var_dic[line[1]] = len(var_dic)
            transcribe = ['0', '*{}'.format(line[2]), '*{}'.format(line[1])]
        # Input is not a variable...
        else:
            print("C")
            # Decompose the commands into a pointer
            # dest variable, sequence (string, space delimited), vardic
            # assemble string from line
            input_str = ''
            for n in line[2:]:
                input_str += "{} ".format(n)
            ptr, pre_string, var_dic, command_tree = dec(input_str, var_dic, debug=debug)
            pretty_print_command_tree(command_tree)
            transcribe = [0, '*{}'.format(ptr), '*{}'.format(line[1])]
            transcribe = [x for x in pre_string.split()] + transcribe

    return transcribe, var_dic


# Add functions to code.
def add_to_code(raw_line, path, index, line, code, var_dic, flag_dic, arr_dic, active_for, debug=False):
    if debug:
        print(f'\t___________________\n\t{index}]\t {line} (Original)')

    flag_val = len(code)  # What is the flag value if we declare one? #TODO: What does this even mean?

    if line[0] == 'flag':
        flag_dic[line[1]] = flag_val

    elif line[0] == '@':
        # TODO: Find a formula to find linear index from multidim index values.
        # Declare an array, add to array_dic
        arr_name = line[1]
        arr_dim = len(line) - 1
        arr_width = int(line[2])
        arr_height = int(line[3])

        arr_len = (arr_width + 1) * (arr_width + 1)
        # TODO: Check if the variable exists before declaring it in memory
        arr_dic[arr_name] = {'name': arr_name, "fulldim": line[2:], "dim": arr_dim, "x": arr_width, 'y': arr_height,
                             'ptr': len(var_dic)}

        # ADD ARRAY POINTERS TO VARDIC
        def add_array(vardic, lst, varindex, arrname):
            mga_lst = [range(z) for z in lst]  # Find all permetutations
            res = list(itertools.product(*mga_lst))
            for combo in res:
                name = '@@_{}_{}'.format(arrname, str(combo))
                vardic[name] = varindex
                varindex = len(vardic)
            return vardic

        vardic = add_array(var_dic, [int(x) for x in line[2:]], var_dic, '{}'.format(arr_name))
        print(arr_dic[arr_name])
        varindex = len(vardic)
        print(vardic)

    elif line[0] == '=':
        # FIRST: Get variable aliases.

        transcribe, var_dic = process_equal(line, var_dic, debug=debug)

        # Command for declaring flags and variables
        # Also declare the value, if it's not declared
    elif line[0] == 'for':  # Add object to active_for

        # TODO: I want to change the syntax of for loops to allow for chained math in the definitoins.
        # TODO: EG, For = n 0 . < n max_iter . = + n 2

        args = [list(y) for x, y in itertools.groupby(line[1:], lambda z: z == '.') if not x]
        # First set of commands are run before the for loop starts.
        # It has to be an initializer, so we will use the process_equal command.
        transcribe_initializer, var_dic = process_equal(args[0], var_dic)

        #var_dic, arg_dic, _ = split_commands_and_args(string, var_dic, debug=debug)  # TODO: Is this really necessary?

        transcribe_terminus, var_dic = process_equal(args[2], var_dic)

        # inc_ptr, pre_string, var_dic, command_tree = dec(arg_dic[3], var_dic, debug=debug)

        title = 'for_{}'.format(len(flag_dic))
        goto_point = 0
        for x in code:
            goto_point += len(x)
        goto_point += len(transcribe_initializer)

        # Copy initializer value into incremental
        active_for.append(
            {'flag': title,
             'initializer': transcribe_initializer,
             'conditional': args[1],
             'incremental': transcribe_terminus,
             'goto_point': goto_point})  # Add 3 because we add a copy operation before the flag

        transcribe = transcribe_initializer



    elif line[0] == 'peek':
        inp = ' '.join(line[1:])


        ptr, pre_string, var_dic, command_tree = dec(inp, var_dic, debug=debug)
        print("PRE STRING")
        print(pre_string)
        transcribe = [x for x in pre_string.split(' ') if x != ''] + [0, '{}'.format(ptr), 0, 4]
    elif line[0] == 'kill':
        transcribe = [5]

    else:  # Invalid command
        print("Compilation error. Terminating.")
        print("Traceback (Most recent call last)")
        print(f'\t File "{path}", line {index}')
        print(f'\t\t{raw_line}')
        l = ' '.join(line)
        print(f'\t\t{l}')
        print(f'\t\tError: {line[0]} is not a valid operator. ')
        exit()

    # add transcibe to code
    if debug:
        print(f'\t{index}]\t {transcribe} (Parsed)\n')
    code += [transcribe]
    return code, var_dic, flag_dic, arr_dic, active_for


# Strip line of comments
def decomment(line):
    # Remove any contents of asset line between (( )). Doesn't work for nested, IE '(( (( )) )). Only (( comment )) .
    firstC = False
    endC = False  # True if the last character was asset )
    ignore = False
    newstr = ''
    for x in line:
        # If we have two successive (, start ignoring.
        # if we have two successive ), stop ignoring.
        if x == ')':
            ignore = endC
            endC = not True
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


def pack(code, var_dic):
    # Take the code and the variable dic and pack it into a single afex structure
    # TODO: If it's a number, make sure to define it's value



    output = []
    for x in code:
        for i in x:
            output.append(i)

    variable_start_point = len(output)


    new_var_dic = {}

    for index, x in enumerate(var_dic):
        try:
            float(x)
            # Set the value appropriately
            new_var_dic['*{}'.format(str(x))] = {'index': variable_start_point + index}
            output.append(float(x))
        except:
            # String var automaticaly set to 0

            new_var_dic['*{}'.format(str(x))] = {'index': variable_start_point + index}
            output.append(0)


    print(output)
    new_output = []
    for i in output:
        if type(i) == str:
            if i[0] == '*': # Replace with pointer value
                new_output.append(new_var_dic[i]['index'])
            else:
                new_output.append(i)
        else:
            new_output.append(i)
    l = len(new_output)
    padding = 512 - l
    padding = ' 0'*padding
    new_output = ' '.join([str(i) for i in new_output]) + padding
    return new_output

# Convert a .rr file to bytecode
def compile(path, dest, debug=False):
    word = []  # This is the list of codes and their arguments.
    code = []  # This is the list of commands that our turing tape exists on.

    var_dic = {}
    flag_dic = {}
    arr_dic = {}

    if debug:
        print("[~~~~~ 1. STARTING CLEANSING ~~~~~}")
    with open(path) as file:
        for index, line in enumerate(file):
            word_line = decomment(line)
            specific_lines = word_line.split(';')
            for sl in specific_lines:
                if sl not in ['', '\n']:
                    operation = []
                    sl = sl.split(' ')
                    temp_op = []  # Just for debug
                    for key in sl:

                        if key not in ['', '\t', '\n']:
                            key = re.sub('\n', '', key)  # Why??
                            if len(key) > 0:
                                temp_op.append(key)
                                operation.append(key)

                    if debug:
                        temp_op = ' '.join(temp_op)
                        print(f'\t{index}]\t {temp_op}')

                    if len(operation) > 0:
                        word.append({'set': operation,
                                     'raw': line})

    indentation_level = 0
    active_for = []  # FILO list of for loops to satisfy
    if debug:
        print("[~~~~~ 2. COMPILING ~~~~~}")
    for index, set in enumerate(word):

        prev_indentation_level = indentation_level
        raw_line = set['raw']
        set = set['set']
        set, indentation_level = indents(set)

        for_loop_satisfy = prev_indentation_level - indentation_level

        # Terminate the for loop if our indentation level has dropped
        if for_loop_satisfy > 0:
            # add conditions to satisfy for loop before continuing.
            for _ in range(for_loop_satisfy):
                print("Active for: ", active_for)
                for_loop_cap = active_for[-1]
                active_for = active_for[:-1]
                code, var_dic = terminate_for(code, for_loop_cap, var_dic)

        code, var_dic, flag_dic, arr_dic, active_for = add_to_code(raw_line,
                                                                   # Unedited, uncommented line in case we have to traceback
                                                                   path,
                                                                   index,
                                                                   set,
                                                                   code,
                                                                   var_dic,
                                                                   flag_dic,
                                                                   arr_dic,
                                                                   active_for,
                                                                   debug=debug)

    # After this: go through the code, assign indexes to variables in var_dic and appropriately re-name in the code list
    print(code)
    print(var_dic)
    decompile(code, var_dic)
    turing_tape = pack(code, var_dic)
    print(turing_tape)
    with open(dest, 'w') as f:
        f.write(turing_tape)