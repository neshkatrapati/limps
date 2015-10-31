# Syntax
## Differences from lisp 
* '<' and '>' instead of '(' and ')'
* '<@ i 10>' sets i to 10
* '<@F foo <f> <* f f>' is a function
* '<foo 1>' is calling that function
* '<@case <= 1 1> 1 <+ 1 2>>' is a case
* '<@while <lt i 10> <@ i <+ i 1>>>' is a while loop

## Using the command line
* print <expr> prints the AST
* time <expr> runs and prints the time taken
* load file_name load that file_name 

# How to run ? 

## Interactive
 ```bash
 python limps.py 
 ```
## With File
  ```bash
  python limps.py -F test.limp
  ```
