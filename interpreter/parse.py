# This file takes aFex wordcode and converts it to aFex bytecode.
import re
import numpy as np
import itertools
from interpreter.decompose_0_0_2b import dec, split_commands_and_args, pretty_print_command_tree, mathop

op = {'==': 0, '!=': 1, '>=': 2, '>': 3, '<=': 4, '<': 5}
reverse_op = {'==': 1, '!=': 0, '>=': 4, '>': 5, '<=': 2, '<': 3}
class Compiler:

    def debug_message(self, message):
        print(message)
        message = str(message).replace('\n', '<br>')
        self.debug_string += str(message) + '<br>'

    def decompile(self, code, var_dic):
        # Prettily prints compiled code so we can validate it.

        self.debug_message("_________________")
        self.debug_message("afex generated")
        self.debug_message("\n\n\n\n")

        for line in code:
            self.debug_message(line)
            solved = False
            command = int(line[0])

            if (len(line) > 1):
                args = line[1:]

                if command == 0:
                    solved = True
                    self.debug_message("COPY {} {} {}".format(args[0], 'TO', args[1]))
                elif command == 1:
                    solved = True

                    self.debug_message("MATHCHAIN {}".format(args))
                elif command == 2:
                    solved = True

                    self.debug_message("COMPARE {}".format(args))
                elif command == 3:
                    solved = True

                    self.debug_message("GOTO {}".format(args))
                elif command == 4:
                    solved = True

                    self.debug_message("self.debug_message {}".format(args))
                elif command == 6:
                    solved = True

                    self.debug_message("IMAGEBUFFER {}".format(args))
                elif command == 7:
                    solved = True

                    self.debug_message("SETPIXEL {}".format(args))

            else:
                if command == 5:
                    solved = True

                    self.debug_message("TERMINATE")
                elif command == 8:
                    solved = True

                    self.debug_message("RENDER ")
                # Single op command with no args
            if not solved:
                self.debug_message("ERROR CANNOT SOLVE")
                self.debug_message(line)
                input()

    # Calculate indentation level of line
    def indents(self, line):
        # Return a line with indentations removed, and return its indentation level
        # Example: extract_indentation([/t/t/thello, world]) == [hello, world], 3
        n = len(line[0]) - len(line[0].lstrip('\t'))
        line = [x.replace('\t', '') for x in line]
        return line, n

    # Declare all legal flag variables. Replace with program indexes before variable interpolation
    def grab_flags(self, word, flag_dic):
        # Returns a dictionary of flags that are legal jump points
        for line in word:
            if line[0] == 'flag':
                # Add to the flag dic
                flag_dic[line[1]] = len(flag_dic)
        return flag_dic

    def terminate_if(self, code, if_cap, var_dic):
        # In this implementaiton we will start by just doing if statements, then try more complex statements later

        self.debug_message("Terminating IF statement")

        goto_end_val = 0

        # When the if statement is terminated we need to retroactively change the goto location to where the indentation occurred.
        for x in code:
            goto_end_val += len(x)

        new_code = []
        # FIXME
        print(if_cap)
        flag = if_cap['flag']
        for x in code:
            step_code = []  # Step that hasn't been concatenated yet
            for y in x:
                if y == f'${flag}':
                    # Replacing the $flag_title placeholder that is set when the if statement is created initially
                    step_code.append(goto_end_val)
                else:
                    step_code.append(y)
            new_code.append(step_code)

        code = new_code
        return code, var_dic


    # Create the appropriate statements to end a for statement
    def terminate_for(self, code, for_loop_cap, var_dic):  # Declare variables and flags first
        self.debug_message("Terminating for loop")
        self.debug_message(for_loop_cap)

        flag_title = for_loop_cap['flag']
        incremental = for_loop_cap['incremental']
        goto_begin = for_loop_cap['goto_begin']  # Where does the end of the for loop return to check the conditional

        code += [incremental, [3, goto_begin]]

        # This section calculates the position of the end of the entire FOR loop
        # (What position the CPU should jump to when the conditional has been met)

        goto_end_val = 0
        print(code)

        for x in code:
            goto_end_val += len(x)

        new_code = []
        for x in code:
            step_code = []  # Step that hasn't been concatenated yet
            for y in x:
                if y == f'${flag_title}':
                    # Replacing the $flag_title placeholder that is set when the for loop is created initially
                    step_code.append(goto_end_val)
                else:
                    step_code.append(y)
            new_code.append(step_code)

        code = new_code
        return code, var_dic

    def process_equal(self, line, var_dic, debug=False):

        self.debug_message(line)
        self.debug_message(var_dic)
        # = Follows the format [dst, src]
        try:
            float(line[2])
            line[2] = float(line[2])
            if line[2] not in var_dic:
                var_dic[line[2]] = len(var_dic)
            # line[2] is the floating point value we need to declare and copy to the line[1] pointer
            if line[1] not in var_dic:
                var_dic[line[1]] = len(var_dic)
            # 0 src dest
            transcribe = ['0', '*{}'.format(line[2]), '*{}'.format(line[1])]

        except:  # input is not a float.
            if line[2] in var_dic:

                if line[1] not in var_dic:
                    var_dic[line[1]] = len(var_dic)
                transcribe = ['0', '*{}'.format(line[2]), '*{}'.format(line[1])]
            # Input is not a variable...
            else:
                # Decompose the commands into a pointer
                # dest variable, sequence (string, space delimited), vardic
                # assemble string from line
                input_str = ''
                for n in line[2:]:
                    input_str += "{} ".format(n)
                ptr, pre_string, var_dic, command_tree = dec(input_str, var_dic, debug=debug)
                var_dic[line[1]] = len(var_dic)

                print("New var dic", var_dic)
                pretty_print_command_tree(command_tree)
                transcribe = [0, '*{}'.format(ptr), '*{}'.format(line[1])]
                transcribe = [x for x in pre_string.split()] + transcribe

        return transcribe, var_dic

    # Add functions to code.
    def add_to_code(self, raw_line, index, line, code, var_dic, flag_dic, arr_dic, active_for_and_if,
                    path='(file path not provided)', debug=False):
        self.debug_message(f'\t___________________\n\tLine {index + 1}]\t{line} (Original)')

        if line[0] == 'flag':
            goto_point = 0
            for x in code:
                goto_point += len(x)
            flag_dic[line[1]] = goto_point
            transcribe = None

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
            self.debug_message(arr_dic[arr_name])
            varindex = len(vardic)
            self.debug_message(vardic)

        elif line[0] == '=':
            # FIRST: Get variable aliases.

            transcribe, var_dic = self.process_equal(line, var_dic, debug=debug)

            # Command for declaring flags and variables
            # Also declare the value, if it's not declared

        elif line[0] == 'for':  # Add object to active_for

            # Step 1: Split list of arguments (Initializer, conditional, incremental)
            args = [list(y) for x, y in itertools.groupby(line[1:], lambda z: z == ',') if not x]
            if len(args) != 3:
                self.debug_message('For loop: Must contain three arguments. Make sure they are separated by commas.')
                print(args)
                raise Exception

            # First set of commands are run before the for loop starts. It has to be an initializer, so we will use the process_equal command.
            transcribe_initializer, var_dic = self.process_equal(args[0], var_dic)

            # TODO: Transcribe initializer should also include the conditional check which should redirect to the END of the loop if the conditinoal is not met,
            # Rather than checking at the end. The issue that arises because of this is that the for loop will always run once no matter what,
            # Even if the conditional is not met, since the conditional redirects toward the BEGINNING of the for loop rather than the END. This could be a tricky one to fix.
            # ( I think this is accomplished - daniel)
            conditional = args[1]


            var_dic, cmd_ptr_dic, conditional_command = split_commands_and_args(' '.join(conditional), var_dic,
                                                                                debug=True)

            if len(cmd_ptr_dic.keys()) != 2:
                self.debug_message(
                    f"Error: Number of arguments {len(cmd_ptr_dic.keys())} in for loop is not the expected value (2).\n"
                    "Check that you have two values in the for loop. ")
                raise Exception  #

            conditional_left = cmd_ptr_dic[0]
            conditional_right = cmd_ptr_dic[1]

            # BREAKDOWN LEFT SIDE

            try:
                float(conditional_left)
                print("It's a float!")
                if conditional_left not in var_dic:
                    var_dic[conditional_left] = len(var_dic)
                    conditional_left = f"*{conditional_left}"
            except:
                # Not a float, could be either a variable or chained math.
                if conditional_left in var_dic:
                    print("It's a variable!")
                    conditional_left = f"*{conditional_left}"
                else:
                    print("It's chainmath!")
                    # Need to do chained math and assign it to a new pointer
                    ptr_left, pre_string_left, var_dic, command_tree = dec(conditional_left, var_dic, debug=True)
                    print(f"Pre string: {pre_string_left}")
                    code += [[x for x in pre_string_left.split(' ') if x is not '']]
                    conditional_left = f'*{ptr_left}'

            # BREAKDOWN RIGHT SIDE

            try:
                float(conditional_right)
                print("It's a float!")
                if conditional_right not in var_dic:
                    var_dic[conditional_right] = len(var_dic)
                    conditional_right = f"*{conditional_right}"
            except:
                # Not a float, could be either a variable or chained math.
                if conditional_right in var_dic:
                    conditional_right = f"*{conditional_right}"
                else:
                    # Need to do chained math and assign it to a new pointer
                    ptr_right, pre_string_right, var_dic, command_tree = dec(conditional_right, var_dic, debug=True)
                    print(f"Pre string: {pre_string_right}")
                    code += [[x for x in pre_string_right.split(' ') if x is not '']]
                    conditional_right = f'*{ptr_right}'

            title = 'for_{}'.format(len(flag_dic))
            flag_dic[title] = 0 # FIXME
            goto_end = f"${title}"

            conditional_code = [2,
                                op[conditional[0]],
                                conditional_left,
                                conditional_right,
                                goto_end]

            transcribe_terminus, var_dic = self.process_equal(args[2], var_dic)

            goto_begin = 0
            for x in code:
                goto_begin += len(x)
            goto_begin += len(transcribe_initializer)

            # Copy initializer value into incremental
            active_for_and_if.append(
                {'type': "for",
                 'flag': title,
                 'initializer': transcribe_initializer,
                 'incremental': transcribe_terminus,
                 'goto_begin': goto_begin,
                 'goto_end': goto_end})

            transcribe = transcribe_initializer + conditional_code

        elif line[0] in ['if']:
            # At the time of writing I think just doing "If" statements is enough to be turing complete
            # Since the corresponding "else" could just be another If statement with the operand negated.

            # I know it's not ideal for now but in the interest of just moving the project forward I'd like to keep it
            # simple.


            self.debug_message("Processing IF statements...")

            # Step 1: Split list of arguments (condition, var 1, var 2)
            operand = line[1]
            assert operand in op, "operand {operand} not a valid boolean operator. "

            # This code is pretty much copy/pasted from the for loop logic so it may be productive to functionalize this section.
            conditional = line[1:]
            print(conditional)

            var_dic, cmd_ptr_dic, conditional_command = split_commands_and_args(' '.join(conditional), var_dic,
                                                                                debug=True)

            if len(cmd_ptr_dic.keys()) != 2:
                self.debug_message(
                    f"Error: Number of arguments {len(cmd_ptr_dic.keys())} in for loop is not the expected value (2).\n"
                    "Check that you have two values in the for loop. ")
                raise Exception  #

            conditional_left = cmd_ptr_dic[0]
            conditional_right = cmd_ptr_dic[1]

            # BREAKDOWN LEFT SIDE

            try:
                float(conditional_left)
                print("It's a float!")
                if float(conditional_left) not in var_dic:
                    var_dic[float(conditional_left)] = len(var_dic)
                conditional_left = f"*{float(conditional_left)}"
            except:
                # Not a float, could be either a variable or chained math.
                if conditional_left in var_dic:
                    print("It's a variable!")
                    conditional_left = f"*{conditional_left}"
                else:
                    print("It's chainmath!")
                    # Need to do chained math and assign it to a new pointer
                    ptr_left, pre_string_left, var_dic, command_tree = dec(conditional_left, var_dic, debug=True)
                    print(f"Pre string: {pre_string_left}")
                    code += [[x for x in pre_string_left.split(' ') if x is not '']]
                    conditional_left = f'*{ptr_left}'

            # BREAKDOWN RIGHT SIDE

            try:
                float(conditional_right)
                print("It's a float!")
                if float(conditional_right) not in var_dic:
                    var_dic[float(conditional_right)] = len(var_dic)
                conditional_right = f"*{float(conditional_right)}"
            except:
                # Not a float, could be either a variable or chained math.
                if conditional_right in var_dic:
                    conditional_right = f"*{conditional_right}"
                else:
                    # Need to do chained math and assign it to a new pointer
                    ptr_right, pre_string_right, var_dic, command_tree = dec(conditional_right, var_dic, debug=True)
                    print(f"Pre string: {pre_string_right}")
                    code += [[x for x in pre_string_right.split(' ') if x is not '']]
                    conditional_right = f'*{ptr_right}'

            title = 'if_{}'.format(len(flag_dic))
            flag_dic[title] = 0  # FIXME ??? - I think it doesn't matter the value since it's automatically calculated when the if is terminated (indentation lost)
            goto_end = f"${title}"

            conditional_code = [2,
                                op[conditional[0]],
                                conditional_left,
                                conditional_right,
                                goto_end]
            print("Conditional code")
            print(conditional_code)

            active_for_and_if.append(
                {'type': "if",
                 'flag': title})


            transcribe = conditional_code


        elif line[0] == 'goto':
            assert line[1] in flag_dic, "Flag not found"
            transcribe = [3, flag_dic[line[1]]]

        elif line[0] == 'print':

            try:
                float(line[1])
                line[1] = float(line[1])
                if line[1] not in var_dic:
                    var_dic[line[1]] = len(var_dic)

                transcribe = [0, '*{}'.format(line[1]), 0, 4]


            except:
                if line[1] in var_dic:
                    transcribe = [0, '*{}'.format(line[1]), 0, 4]

                else:
                    # Process chain math

                    inp = ' '.join(line[1:])
                    ptr, pre_string, var_dic, command_tree = dec(inp, var_dic, debug=debug)

                    transcribe = [x for x in pre_string.split(' ') if x != ''] + [0, '*{}'.format(ptr), 0, 4]

        elif line[0] == "imagebuffer":
            # Send signal to create imagebuffer x*y
            # Just need to process two variables or chain math and send that to the thing

            # This code is pretty much copy/pasted from the for loop logic so it may be productive to functionalize this section.

            var_dic, cmd_ptr_dic, conditional_command = split_commands_and_args("~ " +" ".join(line[1:]), var_dic,
                                                                                debug=True)


            conditional_left = cmd_ptr_dic[0]
            conditional_right = cmd_ptr_dic[1]
            print("\033[0mCONDITIONALS: " + conditional_left, "------", conditional_right)
            # BREAKDOWN LEFT SIDE

            try:
                float(conditional_left)
                print("It's a float!")
                if float(conditional_left) not in var_dic:
                    var_dic[float(conditional_left)] = len(var_dic)
                conditional_left = f"*{float(conditional_left)}"
            except:
                # Not a float, could be either a variable or chained math.
                if conditional_left in var_dic:
                    print("It's a variable!")
                    conditional_left = f"*{conditional_left}"
                else:
                    print("It's chainmath!")
                    # Need to do chained math and assign it to a new pointer
                    ptr_left, pre_string_left, var_dic, command_tree = dec(conditional_left, var_dic, debug=True)
                    print(f"Pre string: {pre_string_left}")
                    code += [[x for x in pre_string_left.split(' ') if x is not '']]
                    conditional_left = f'*{ptr_left}'

            # BREAKDOWN RIGHT SIDE

            try:
                float(conditional_right)
                print("It's a float!")
                if float(conditional_right) not in var_dic:
                    var_dic[float(conditional_right)] = len(var_dic)
                conditional_right = f"*{float(conditional_right)}"
            except:
                # Not a float, could be either a variable or chained math.
                if conditional_right in var_dic:
                    conditional_right = f"*{conditional_right}"
                else:
                    # Need to do chained math and assign it to a new pointer
                    ptr_right, pre_string_right, var_dic, command_tree = dec(conditional_right, var_dic, debug=True)
                    print(f"Pre string: {pre_string_right}")
                    code += [[x for x in pre_string_right.split(' ') if x is not '']]
                    conditional_right = f'*{ptr_right}'


            transcribe =        [6,
                                conditional_left,
                                conditional_right]


        elif line[0] == "setpixel":
            # setpixel x y 1/0

            # Send signal to set pixel of image buffer
            # we need to add an assertion that there's a buffer and the x/y falls in range.


            # Just need to process two variables or chain math and send that to the thing

            # This code is pretty much copy/pasted from the for loop logic so it may be productive to functionalize this section.

            var_dic, cmd_ptr_dic, conditional_command = split_commands_and_args("~ " + " ".join(line[1:]), var_dic,
                                                                                debug=True)

            conditional_left = cmd_ptr_dic[0]
            conditional_right = cmd_ptr_dic[1]
            print("\033[0mCONDITIONALS: " + conditional_left, "------", conditional_right, "--------", cmd_ptr_dic[2])
            # BREAKDOWN LEFT SIDE

            try:
                float(conditional_left)
                print("It's a float!")
                if float(conditional_left) not in var_dic:
                    var_dic[float(conditional_left)] = len(var_dic)
                conditional_left = f"*{float(conditional_left)}"
            except:
                # Not a float, could be either a variable or chained math.
                if conditional_left in var_dic:
                    print("It's a variable!")
                    conditional_left = f"*{conditional_left}"
                else:
                    print("It's chainmath!")
                    # Need to do chained math and assign it to a new pointer
                    ptr_left, pre_string_left, var_dic, command_tree = dec(conditional_left, var_dic, debug=True)
                    print(f"Pre string: {pre_string_left}")
                    code += [[x for x in pre_string_left.split(' ') if x is not '']]
                    conditional_left = f'*{ptr_left}'

            # BREAKDOWN RIGHT SIDE

            try:
                float(conditional_right)
                print("It's a float!")
                if float(conditional_right) not in var_dic:
                    var_dic[float(conditional_right)] = len(var_dic)
                conditional_right = f"*{float(conditional_right)}"
            except:
                # Not a float, could be either a variable or chained math.
                if conditional_right in var_dic:
                    conditional_right = f"*{conditional_right}"
                else:
                    # Need to do chained math and assign it to a new pointer
                    ptr_right, pre_string_right, var_dic, command_tree = dec(conditional_right, var_dic, debug=True)
                    print(f"Pre string: {pre_string_right}")
                    code += [[x for x in pre_string_right.split(' ') if x is not '']]
                    conditional_right = f'*{ptr_right}'

            transcribe = [7,
                          conditional_left,
                          conditional_right,
                          cmd_ptr_dic[2]]

        elif line[0] == "render":
            transcribe = [8]


        elif line[0] == 'kill':
            transcribe = [5]

        else:  # Invalid command
            self.debug_message("Compilation error. Terminating.")
            self.debug_message("Traceback (Most recent call last)")
            self.debug_message(f'\t File "{path}", line {index}')
            self.debug_message(f'\t\t{raw_line}')
            l = ' '.join(line)
            self.debug_message(f'\t\t{l}')
            self.debug_message(f'\t\tError: {line[0]} is not a valid operator. ')
            exit()

        # add transcibe to code
        if debug:
            self.debug_message(f'\t{index}]\t {transcribe} (Parsed)\n')
        if transcribe is not None:
            code += [transcribe]
        return code, var_dic, flag_dic, arr_dic, active_for_and_if

    # Strip line of comments
    def decomment(self, line):
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

    def pack(self, code, var_dic):
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

        self.debug_message(output)
        new_output = []
        for i in output:
            if type(i) == str:
                if i[0] == '*':  # Replace with pointer value
                    new_output.append(new_var_dic[i]['index'])
                else:
                    new_output.append(i)
            else:
                new_output.append(i)
        l = len(new_output)
        padding = 512 - l
        padding = ' 0' * padding
        new_output = ' '.join([str(i) for i in new_output]) + padding
        return new_output

    # Convert a .rr file to bytecode
    def compile(self, src, dest='', mode='file', debug=False):
        # This function takes in human readable River code, and EITHER returns a
        # file to the destination path or
        # Returns a JSON with compiled bytecode (For API mode),
        assert mode in ['api', 'file'], 'Mode must be in API mode or FILE mode'

        self.debug_string = ''  # Returned as part of the compilation process to the frontend for insight into compiler operations if something fails.

        path = ''
        if mode == 'file':
            path = src
            src = []
            with open(path) as file:
                for line in file:
                    src.append(line)
        elif mode == 'api':
            path = 'river_ide.rr'
            src = src.split('\n')
        word = []  # This is the list of codes and their arguments.
        code = []  # This is the list of commands that our turing tape exists on.

        var_dic = {}
        flag_dic = {}
        arr_dic = {}

        self.debug_message("[~~~~~ 1. STARTING CLEANSING ~~~~~]")

        for index, line in enumerate(src):
            word_line = self.decomment(line)
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

                    temp_op = ' '.join(temp_op)
                    self.debug_string += f'\t{index}]\t {temp_op} \n'

                    if len(operation) > 0:
                        word.append({'set': operation,
                                     'raw': line})

        indentation_level = 0
        active_for_and_if = []  # FILO list of for loops and if statements to satisfy

        self.debug_string += "[~~~~~ 2. COMPILING ~~~~~]"

        for index, set in enumerate(word):

            prev_indentation_level = indentation_level
            raw_line = set['raw']
            set = set['set']
            set, indentation_level = self.indents(set)

            for_loop_and_if_satisfy = prev_indentation_level - indentation_level

            # Terminate the for loop if our indentation level has dropped
            if for_loop_and_if_satisfy > 0:
                # add conditions to satisfy for loop before continuing.
                for _ in range(for_loop_and_if_satisfy):
                    self.debug_string += "Active for: {}".format(active_for_and_if)
                    for_loop_cap = active_for_and_if[-1]
                    active_for_and_if = active_for_and_if[:-1]

                    if for_loop_cap['type'] == 'for':
                        code, var_dic = self.terminate_for(code, for_loop_cap, var_dic)
                    elif for_loop_cap['type'] == 'if':
                        code, var_dic = self.terminate_if(code, for_loop_cap, var_dic)

            code, var_dic, flag_dic, arr_dic, active_for_and_if = self.add_to_code(raw_line,
                                                                                   # Unedited, uncommented line in case we have to traceback
                                                                                   index,
                                                                                   set,
                                                                                   code,
                                                                                   var_dic,
                                                                                   flag_dic,
                                                                                   arr_dic,
                                                                                   active_for_and_if,
                                                                                   path=path,
                                                                                   debug=debug)

        # After this: go through the code, assign indexes to variables in var_dic and appropriately re-name in the code list
        self.debug_message(code)
        self.debug_message(var_dic)
        self.decompile(code, var_dic)
        turing_tape = self.pack(code, var_dic)
        self.debug_message(turing_tape)
        if mode == 'file':
            with open(dest, 'w') as f:
                f.write(turing_tape)
        else:
            json_return_struc = {
                'compiled': turing_tape,
                'debug': self.debug_string
            }
            return json_return_struc
