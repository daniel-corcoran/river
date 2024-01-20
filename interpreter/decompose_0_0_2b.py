
mathop = {'+': 0, '-': 1, '*': 2, '/': 3, '^': 4}



def pretty_print_command_tree(command_tree, depth = 0):
    print(command_tree)
    # print(command_tree)
    print("\t" * depth, command_tree['op'], command_tree['pointer'])
    # print("\t" * depth, '|')
    for i in range(len(command_tree['args'])):
        if type(command_tree['args'][i]) != list:
            print("\t" * depth, '|~', command_tree['args'][i] )

        else:
            print("\t" * depth, '|~', end='')
            pretty_print_command_tree(command_tree['args'][i], depth = depth + 1)


def create_chained_math(operator, values, var_dic, debug=False):
    if debug:
        print("Creating chained math. Operator: {} arguments: {}".format(operator, values))
    # All values must be in the var dic.
    # Returns pre-sequence code and variable name and var_dic
    chain_loc = 'chain_{}'.format(len(var_dic)) # Variable name for the output of our chain operation

    var_dic[chain_loc] = len(var_dic)
    my_str = '1 {} *{} *{} *{} '.format(mathop[operator], values[0], values[1], chain_loc) # Add the first two arguments

    for val in values[2:]:
        my_str += '1 {} *{} *{} *{} '.format(mathop[operator], chain_loc, val, chain_loc)

    return chain_loc, my_str, var_dic


def split_commands_and_args(string, var_dic, debug=False):
    if debug:
        print("\t\t\t[~~~~~ SPLITTING COMMANDS AND ARGS ~~~~~]")
    print(f"Var dic at beginning: {var_dic}")
    # Splits the command, and arguments, into individual pieces.

    cmd_depth = 0
    cur_cmd = 0 # The argument we are currently processing.
    print(string)
    first_command = string[0] # The operation occuring on the arguments
    string = string[1:] # The full, un-split arguments.
    cmd_ptr_dic = {}
    # print(string.split())
    for arg in string.split():
        if debug:
            print("\t\t\tCMD DEPTH: {} ARG: {}".format(cmd_depth, arg))
        try: # TODO: Why are we using try/catch exceptions here?

            if cmd_depth == 0: # Declare a number or variable as an individual argument only if cmd depth is at base
                float(arg)
                if arg not in var_dic:
                    print(f"{arg} is not in the var dic {var_dic}.")
                    var_dic[float(arg)] = len(var_dic)
                cur_cmd = len(cmd_ptr_dic)
                # arg = '*{}'.format(arg)
                cmd_ptr_dic[cur_cmd] = ''
        except:
            if cmd_depth == 0 and arg in var_dic:
                cur_cmd = len(cmd_ptr_dic)
                cmd_ptr_dic[cur_cmd] = ''

        if arg in mathop:
            if cmd_depth == 0:
                cur_cmd = len(cmd_ptr_dic)
                cmd_ptr_dic[cur_cmd] = '' # Represents the string for the argument by pointer (starting at 0)
            cmd_depth += 1
            if debug:
                print("\t\t\t", cur_cmd, cmd_depth, "{}New argument branch: ".format("\t "* cmd_depth), arg, "Pointer result: ", cur_cmd)
        if arg == '.':
            if debug:
                print("\t\t\t", cur_cmd, cmd_depth, "{} Argument pipe ended".format("\t "* cmd_depth))
            cmd_depth -= 1
            cmd_ptr_dic[cur_cmd] += arg + ' '

        else:

            if debug:
                print("\t\t\t", cur_cmd, cmd_depth, "\t| "* cmd_depth, arg)
            # if cur_cmd is not None:
            cmd_ptr_dic[cur_cmd] += arg + ' '

    print(f"Var dic at breakpoint: {var_dic}")
    # Remove commands where the last element is a period
    for i in cmd_ptr_dic:
        if debug:
            print(i, cmd_ptr_dic[i])
        if '.' in cmd_ptr_dic[i].split()[-1]:
            try:
                float(cmd_ptr_dic[i])
            except:
                if debug:
                    print("Removing . from {}".format(cmd_ptr_dic[i]))
                nw_str = ''
                for x in cmd_ptr_dic[i].split()[:-1]:
                    nw_str += x + ' '

                cmd_ptr_dic[i] = nw_str
        if cmd_ptr_dic[i][-1] == ' ':
            cmd_ptr_dic[i] = cmd_ptr_dic[i][:-1]

    if debug:
        print("Output: var_dic={}, cmd_ptr_dic={}, first_comand={}".format(var_dic, cmd_ptr_dic, first_command))
    return var_dic, cmd_ptr_dic, first_command


def decompose(arguments, var_dic, debug = False):

    command_tree = {'op': None,
                    'args': [],
                    'pointer': None} # Can we build this? Arg1 and arg2 are either command trees, variables or values

    if debug:
        print("\t\t\t\t______________________________\n"
              "\t\t\t\tDecomposing:\n"
              "\t\t\t\t arg: {}\n"
              "\t\t\t\t var_dic: {}\n"
              "\t\t\t\tIterating through arguments in debug...\n"
              "\t\t\t\t______________________________\n".format(arguments, var_dic))

    # Converts a string of arguments into a pointer and pre-cursor string.
    var_dic, cmd_ptr_dic, operator = split_commands_and_args(arguments, var_dic)
    command_tree['op'] = operator


    # TODO: Get the variable names for the current operator.
    # Save to list 'values'
    values = []
    cmd_string = '' # string of pre-cursor commands to satisfy

    for arg in cmd_ptr_dic:
        if debug:
            print("\t\t\t\tCMD_PTR_DIC: ", cmd_ptr_dic)
        # We need to get the variable names for these values.
        try:
            cmd_ptr_dic[arg] = float(cmd_ptr_dic[arg])
            cmd_no_space = float(cmd_ptr_dic[arg])
        except:
            cmd_no_space = str(cmd_ptr_dic[arg]).replace(' ', '')


        # TODO: Iterate through the lists, trying to cast to float all values to check if they exits
        # The reason is because checking if the comand exists in the var dic may not work for floating point values
        # Due to weird stuff, in other words if cmd_no_space in var_dic doesn't work for floats.
        found = False
        for i in var_dic:
            try:
                i = float(i)
                cmd = float(cmd_no_space)
                if abs(i - cmd) < 0.00000001:
                    found = True
                    values.append(cmd_no_space)
                    command_tree['args'].append(cmd_no_space)
                    break
            except:
                if i == cmd_no_space:
                    found = True
                    values.append(cmd_no_space)
                    command_tree['args'].append(cmd_no_space)



        if not found:
            if debug:
                print("\t\t\t\tPointer record:", var_dic, "value that wasn't found: ", str(cmd_ptr_dic[arg]))

            result_ptr, pre_string, var_dic, sub_tree = decompose(cmd_ptr_dic[arg], var_dic, debug=debug)
            command_tree['args'].append(sub_tree)

            if debug:
                print(" -> {}".format(result_ptr))
            cmd_string = pre_string + cmd_string
            values.append(result_ptr)

    self_ptr, math_chain, var_dir = create_chained_math(operator, values, var_dic, debug=debug)
    cmd_string += math_chain
    if debug:
        print("Decomposed {} into pre-string {}".format(arguments, cmd_string))
    command_tree['pointer'] = self_ptr
    return self_ptr, cmd_string, var_dic, command_tree
    # The decompose function recursively returns a sequence of commands to process arguments
    # Returns a variable name where the output is stored, and the new var_dic


def dec(arguments, var_dic, debug = False):
    empty_tree = {'op': None,
                    'args': [],
                    'pointer': None}
    # Determine here whether we are handling a variable, float, or some
    # nested operations involving either.
    if debug:
        print("\t\t[~~~~~~ DECOMPOSING ~~~~~~] ")

        print("\t\tfn dec: arg: {} var_dic: {}".format(arguments, var_dic))
    # Return variable name as self PTR if in var dic, or
    try:
        float(arguments)
        # Continue if the argument is a number.
        if arguments not in var_dic:
            var_dic[arguments] = len(var_dic)
        return '*{}'.format(arguments), '', var_dic, empty_tree
    except:
        # Not a floating number. Is it already a variable?
        if arguments.replace(' ', '') in var_dic:
            return '*{}'.format(arguments), '', var_dic, empty_tree
        else:
            return decompose(arguments, var_dic, debug = debug)


# print(dec('/ + a b c + 1 + a b . . . * 2 a f', {'a': 1, 'b': 2, 'c': 3, 'd': 0, 'e': 0, 'f': 0}, debug=True))
#_, _, _, command_tree = dec('* + a + b c . . - a b .', {'a': 1, 'b': 2, 'c': 3, 'd': 0, 'e': 0, 'f': 0}, debug=False)
#pretty_print_command_tree(command_tree)

#a, b, c, d = dec('+ a - a + b c', {'a': 1, 'b': 2, 'c': 3}, debug=False)
#print("")
