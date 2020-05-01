<p style="text-align: center;">![River logo](river/river.jpg)</p>



Each program can only be 64 'commands' long. Each command can be represented as a long double. Coming soon isvariable program size, but program size will be fixed at compile time.
In an afex program, every value is a pointer. This means that an afex program can change any aspect of itself after compile-time.

COMMANDS: 
0. Copy [a] [b] (Overwrites the value at index B with the value at index A)
1. Arithmatic (operator) ($value_a) ($value_b)
2. Comparator (operator) ($value_a) ($value b) (else$)
    (If value_a operator value_b, continue, else set $index as else$)
3. goto_index  
4. Print register 0
5: stop terminate

ARITHMATIC OPERATORS:
0: Addition
1. Subtraction
2. Product 
3. Quotient
4. Power

COMPARISON OPERATORS:
0. Equals         (==)
1. Not            (!=)
2. Greater/Equal  (>=)
3. Greater        (> )
4. Less/Equal     (<=)
5. Less           (< )

Example: Calculating Pi
0 1 4 60 62 56 1 2 62 58 55 1 0 59 55 55 1 3 56 55 55 1 2 57 55 55 1 0 55 0 0 1 0 62 59 62 2 3 62 63 1 4 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 2 1 -1 0 0 100000000 

0 is the display register, and cannot contain a executable function. All programs start running at index 1. 

Translated: 
0               // DisplayRegister      $0
1 4 60 62 56    // Arithmatic Power     $60, $62, sto $56
1 2 62 58 55    // Arithmatic Product   $62, $58, sto $55
1 0 59 55 55    // Arithmatic Add       $59, $55, sto $55  
1 3 56 55 55    // Arithmatic Quotient  $56, $55, sto $55
1 2 57 55 55    // Arithmatic Product   $57, $55, sto $55
1 0 55 0 0      // Arithmatic Add       $55, $0,  sto $0
1 0 62 59 62    // Arithmatic Add       $62, $59, sto $62
2 3 62 63 1     // Comparator Greater   $62, $63, else $1
4               // Output DisplayRegister
5               // Terminate
0 0 0 0 0 0 0   // Empty
0 0 0 0 0 0 0   // Empty
4 2 1 -1 0 0    // $57, $58, $59, $60, $62, $63
100000000       // $63 (This is the number of sums to calculate. Higher = higher precision)
