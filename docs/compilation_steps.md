# Compilation Steps

This document aims to answer the question, how does river code get compiled to afex bytecode step by step?


## Compiler Class

The compiler is represented as a class in the parse.py file. 


Compilation can happen in either API more or FILE mode. This just tells the compiler whether it should
get its source from a file or as a string argument. 

## Cleansing and Sanitization

The first and most trivial step of compilation is scanning the source code for comments and empty lines and removing them. 

If multiple lines are inlined via a semicolon, we split those into separate lines as well. 

## First pass iteration

For each line of the code, we track it's indentation level (to see for instance if we have exited out of an if or for statement). 

We keep track of a FIFO data structure containing all the "unfinished" ifs and for statements. 

If the indentation level decreases, we pop a struct with metadata about the last if/for loop and do some work to terminate it. 

TODO: Write a wiki page explaining for loops and if statements. 

Afer this, in the `add_to_code` function we convert any operations into chunks of bytecode. This step includes chained math which 
I think deserves its own wiki entry lol. 

## Second pass - packing

In the creation of the bytecode we may have assigned several temporary variables that had not been assigned pointers yet. 

Those variables and their initialization values are stored in the var_dic variable. 

This assigns all variables a specific memory location and makes sure to update the bytecode with the updated memory locations. 

