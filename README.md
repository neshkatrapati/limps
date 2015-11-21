# Syntax
## Differences from lisp 
```python
* '<' and '>' instead of '(' and ')'
* '<@ i 10>' sets i to 10
* '<@F foo <f> <* f f>' is a function
* '<foo 1>' is calling that function
* '<@case <= 1 1> 1 <+ 1 2>>' is a case
* '<@while <lt i 10> <@ i <+ i 1>>>' is a while loop
* Lists are just blocks of code which are not yet executed. so, lists are parts of asts
* '`<1 2 3 4>' is a list
* '<@~ `<+ 1 2>>' 'executes' the list and gives out 3
* '<: `<1 2 3 4> 1>' gives 2, ':' is indexing operator
* '<# `<1 2>>' gives 2, '#' is length operator
* '<:/ `<1 2 3 4> 1 2>' gives `<2 3>, :/ is a slicing operator
```

Look at respective .limp files for more docs
- basefuncs.limp : Basic functions
- listops.limp : List operations
- assoc.limp : Assoicative Lists and its functions
- Type.limp : Types and their related functions

None of these files are included by default (not even in the REPL) to use them,
```python
<import file_name_without_dotlimp>
like this <import basefuncs>
```

## Fun facts ##
* Lists are just code not executed. They are parts of the AST
* They can be executed.
* Associative Lists are made up of lists
* Types are made up of Associative Lists
* When you call Type, it returns a function which returns an Assoc

## Using the command line ##
```python
* print <expr> prints the AST
* time <expr> runs and prints the time taken
```
# How to run ? 

## Interactive
 ```bash
 python limps.py 
 ```
## With File
  ```bash
  python limps.py test.limp
  ```
