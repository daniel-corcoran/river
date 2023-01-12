![River Programming Language](img/river.jpg)



Example program: Calculate pi via Leibniz  summation
```

= sum 0;
= max_iter 10000000;

for = n 0 .  < n max_iter . = n + n 1
	= sum + sum * 4 / ^ -1 n . + * n 2 . 1
	peek sum

kill
Output: 3.14159
```

## Usage
```shell

# Compile a program to bytecode
python3 compile.py projects/for_loops/pi_chained.rr projects/for_loops/pi_chained.a

# Execute bytecode using the AFEX interpreter https://github.com/daniel-corcoran/afex
./bin/main projects/for_loops/pi_chained.a
```


## Programming specification

1. Declaring variables

    `= [variable name] [value]`
    
    Example:
    ```
   = pi 3.14159
   print pi
   
   output: 3.14159
   ```
2. Declaring flags
    
    `flag [flag name]`
    
    Flags serve as reference points that your code can jump to at any point.
    
    Example: 
    ```
   (( Note - this is currently not implemented ))
    = a 5 . 
    = my_flag flag;
    = a + 5 a . .
    print a
    goto my_flag
  
    output: 10 20 40 80 160 ... ...
    ``` 
    
3. Ternary operators
    
   `[operator] [variable 1] [variable 2] [flag name]`
   
   
Ternary operators     

Legal operators: != == <= < >= >`
If (variable 1) operator (variable_2) is true, continue to next line.
    
If false, go to the flag statement.
    
Example:


   byteword 64 (( Allocate 64 spaces ))
   = counter 0
   = max_count 10
   = 1 1 (( Since all values must be variables, we define integers individually. ))
   flag my_flag (( We can jump to this point from anywhere in the code. ))
+ 1 counter counter
print counter
`> counter max_count my_flag`
kill
> 
   
   Output: 1 2 3 4 5 6 7 8 9 10
  
4. Mathematical operations
    
   the way math works in this language is pretty peculiar, I will do a writeup on it soon

    `[operator] [variable 1] [variable 2] [destination variable]`
    
    Legal operators: `^ - + * / `
    
    Example:
    ```
   = a 5;
   = b 7;
   = c 0;
   = + a b c ; (( a + b = c ))
   = + a - b c . . d; (( a + ( b - c ) = d))
    ```
5. FOR loops
   ### Note, a major update has changed the way this works as well, see the pi example for syntax, a writeup is needed  
   ```
   = iter 3
   for = a 0 . < a iter . = a + a 1
       print a
       for = b 0 . < b iter . = b + b 1
           print b
   
   Output: 0 0 1 2 3 1 0 1 2 3 2 1 2 3
    ```                
   
   
7. Multidimensional arrays
``` 
   (( Note - this is currently not implemented yet ))
    @ my_array 10 10
    for a 0 10
        for b 0 10
            my_array a b a
    print my_array
    
    Output:
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
    0 1 2 3 4 5 6 7 8 9
```                                                                                      