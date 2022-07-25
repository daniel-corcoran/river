mathop = {'+': 0, '-': 1, '*': 2, '/': 3, '^': 4}


def create_chained_math(operator, values, var_dic):
    print("Creating chained math. Operator: {} Values: {}".format(operator, values))
    # All values must be in the var dic.
    # Returns pre-sequence code and variable name and var_dic
    chain_loc = 'chain_{}'.format(len(var_dic)) # Variable name for the output of our chain operation

    var_dic[chain_loc] = len(var_dic)
    my_str = '1 {} *{} *{} *{} '.format(mathop[operator], values[0], values[1], chain_loc) # Add the first two arguments

    for val in values[2:]:
        my_str += '1 {} *{} *{} *{} '.format(mathop[operator], chain_loc, val, chain_loc)

    return chain_loc, my_str, var_dic


def split_commands_and_args(string, var_dic, debug=False):
    # Splits the command, and arguments, into individual pieces.
    cmd_depth = 0
    cur_cmd = 0 # The argument we are currently processing.
    first_command = string[0] # The operation occuring on the arguments
    string = string[1:] # The full, un-split arguments.
    cmd_ptr_dic = {}
    #print(string.split())
    for arg in string.split():
        try:
            if cmd_depth == 0: # Declare a number or variable as an individual argument only if cmd depth is at base
                float(arg)
                if arg not in var_dic:
                    var_dic[float(arg)] = len(var_dic)
                cur_cmd = len(cmd_ptr_dic)
                #arg = '*{}'.format(arg)
                cmd_ptr_dic[cur_cmd] = ''
        except:
            if cmd_depth == 0:
                if arg in var_dic:
                    cur_cmd = len(cmd_ptr_dic)
                    cmd_ptr_dic[cur_cmd] = ''
            else:
                pass
            # now we know it's not a float...
        if arg in mathop:
            if cmd_depth == 0:
                cur_cmd = len(cmd_ptr_dic)
                cmd_ptr_dic[cur_cmd] = '' # Represents the string for the argument by pointer (starting at 0)
            cmd_depth += 1
            if debug:
                print(cur_cmd, cmd_depth, "{}New argument branch: ".format("\t"* cmd_depth), arg, "Pointer result: ", cur_cmd)
        if arg == '.':
            if debug:
                print(cur_cmd, cmd_depth, "{} Argument pipe ended".format("\t"* cmd_depth))
            cmd_depth -= 1
            if cmd_depth == 2:
                cur_cmd += 1
                cmd_ptr_dic[cur_cmd] = '' # Represents the string for the argument by pointer (starting at 0)
            cmd_ptr_dic[cur_cmd] += arg + ' '

        else:
            try:
                if debug:
                    print(cur_cmd, cmd_depth, "\t|"* cmd_depth, arg)
                #if cur_cmd is not None:
                cmd_ptr_dic[cur_cmd] += arg + ' '
            except Exception as e:
                print(e)
                print(arg)
                exit()

    # Remove commands where the last element is a period
    for i in cmd_ptr_dic:
        print(i, cmd_ptr_dic[i])
        if '.' in cmd_ptr_dic[i].split()[-1]:
            print("Removing . from {}".format(cmd_ptr_dic[i]))
            nw_str = ''
            for x in cmd_ptr_dic[i].split()[:-1]:
                nw_str += x + ' '
            cmd_ptr_dic[i] = nw_str
    print(cmd_depth)
    return var_dic, cmd_ptr_dic, first_command


def decompose(arguments, var_dic, debug = False):
    if debug:
        print("Decomposing {}".format(arguments))
    var_dic, cmd_ptr_dic, operator = split_commands_and_args(arguments, var_dic)
    # TODO: Get the variable names for the current operator.
    # Save to list 'values'
    values = []
    cmd_string = '' # string of pre-cursor commands to satisfy

    for arg in cmd_ptr_dic:
        print("CMD_PTR_DIC: ", cmd_ptr_dic)
        # We need to get the variable names for these values.
        try:
            cmd_ptr_dic[arg] = float(cmd_ptr_dic[arg])
        except:
            pass

        try:
            cmd_no_space = float(cmd_ptr_dic[arg])
        except:
            cmd_no_space = str(cmd_ptr_dic[arg]).replace(' ', '')

        if cmd_no_space in var_dic:
                values.append(cmd_no_space)
        else:
            print("Pointer record:", var_dic, "value that wasn't found: ", str(cmd_ptr_dic[arg]))

            result_ptr, pre_string, var_dic = decompose(cmd_ptr_dic[arg], var_dic)
            print(" -> {}".format(result_ptr))
            cmd_string = pre_string + cmd_string
            values.append(result_ptr)

    self_ptr, math_chain, var_dir = create_chained_math(operator, values, var_dic)
    cmd_string += math_chain

    return self_ptr, cmd_string, var_dic
    # The decompose function recursively returns a sequence of commands to process arguments
    # Returns a variable name where the output is stored, and the new var_dic


def dec(arguments, var_dic, debug = False):
    print("Decomposing: {}".format(arguments))
    # Return variable name as self PTR if in var dic, or
    try:
        float(arguments)
        # Continue if the argument is a number.
        if arguments not in var_dic:
            var_dic[arguments] = len(var_dic)
        return '*{}'.format(arguments), '', var_dic
    except:
        # Not a floating number. Is it already a variable?
        if arguments in var_dic:
            return '*{}'.format(arguments), '', var_dic
        else:
            return decompose(arguments, var_dic, debug = False)


print(dec('/ + a b c + 1 + a b . . . * 2 a', {'a': 1, 'b': 2, 'c': 3, 'd': 0, 'e': 0, 'f': 0}))