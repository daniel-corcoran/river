![](river.jpg)



1. Declaring variables

    `declare [variable name] [value]`
    
    Example:
    ```
   byteword 64;
   declare pi 3.14159
   peek pi
   
   output: 3.14159
   ```
2. Declaring flags
    
    `declare [flag name] flag`
    
    Flags serve as reference points that your code can jump to at any point.
    
    Example: 
    ```
    byteword 64;
    declare 5 5;
    declare my_flag flag;
    + 5 5 5
    peek 5 
    $ my_flag
    kill;
   
    output: 10 20 40 80 160 ... ...
    ```
    
3. Ternary operators
    
    `flag [operator] [variable 1] [variable 2] [flag name]`
    
    Legal operators: `!= == <= < >= >`
    If (variable 1) operator (variable_2) is true, continue to next line.
    
    If false, go to the flag statement.
    
    Example:
    ```
   byteword 64; (( Allocate 64 spaces ))
   declare counter 0;
   declare max_count 10;
   declare 1 1; (( Since all values must be variables, we define integers individually. ))
   declare flag my_flag; (( We can jump to this point from anywhere in the code. ))
   + 1 counter counter;
   peek counter;
   > counter max_count my_flag;
   kill;
   
   Output: 1 2 3 4 5 6 7 8 9 10
   
    ```
4. Mathematical operations
    
    `[operator] [variable 1] [variable 2] [destination variable]`
    
    Legal operators: `^ - + * / `
    
    Example:
    ```
   byteword 64; (( Allocate 64 spaces ))
   declare a 5;
   declare b 7;
   declare c 0;
   + a b c;
   peek c;
   kill;
   
   Output: 13
   
    ```
    
                                                                                                                   