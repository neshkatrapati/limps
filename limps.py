#My Lisp Implementation

import sys
from stree import *
from primitives import *
from parser  import Parser
from helpers import *
import shlex
import cmd
from copy import deepcopy
from time import time


def evaluate(node, symbols):
    #print "Node", node, node.type

    if node.type == "__quote__":
        #print "I goes in"
        m = Method(None, node.children[0])
        return m

    if len(node.children) == 0:
        if node.type == "__meta__":
            return None
        return evaluate_expr([node.node], symbols)
    else:
        agg = []
        E = True
        rem = []
        flags = {"case": False,
                 "def":False,
                 "while":False,
                 "sdef": False,
                 "unp":False,
                 "quote": False}

        case_stat = False
        for index, child in node.children.items():
            res = None
            #print index, child
            if child.type == "__quote__":
                agg.append(child)
                continue


            if index == 0:
                if child.node == "@":
                    flags["sdef"] = True
                if child.node == "@F":
                    #print "Im in", child
                    flags["def"] = True
                    res = child
                elif child.node == "@case":
                    flags['case'] = True
                    #print node.children
                elif child.node == "@while":
                    flags["while"] = True
                elif is_method(child.node, symbols) == False:
                    #print "Going in"
                    res = evaluate(child, symbols)
                    agg.append(res)
                else:
                    agg.append(child.node)

            elif index == 1 and flags["sdef"]:
                if child.node in symbols:
                    agg.append(child.node)
                else:
                    agg.append(evaluate(child, symbols))
            elif index == 1 and flags["case"]:
                res = evaluate(child, symbols)
                case_stat = convert_to_bool(res)
                #print case_stat
            elif index == 1 and flags["while"] == True:
                res = True
                while res:
                    res = evaluate(child, symbols)
                    res = convert_to_bool(res)
                    if res == False:
                        break
                    e = evaluate(node.children[index + 1], symbols)

            elif index == 2 and flags["while"] == True:
                pass

            elif flags['case'] == True:
                if case_stat and index == 2:
                    agg.append(evaluate(child, symbols))
                elif case_stat == False and index == 3:
                    agg.append(evaluate(child, symbols))
                # else:
                #     rem.append(child)

            elif flags["def"] == True:
                #print "Im in"
                res = child
                rem.append(res)
            else:
                res = evaluate(child, symbols)
                agg.append(res)
        #print agg, rem
        if len(rem) > 0:
            #print "Setting rem"
            return set_rem(rem, symbols)
            #return evaluate_expr(agg)
        elif len(agg) > 0:
            #print "Agg", agg
            return evaluate_expr(agg, symbols)



def evaluate_expr(expr, symbols):
    #print expr
    if len(expr) > 1:
        if expr[0] in functions:
            if expr[0] in ["@", "@!"]:
                t = functions[expr[0]](expr[1:], symbols)
            else:
                t = functions[expr[0]](expr[1:])
            if type(t) == STREE and t.type == "__quote__":
                return t
            else:
                return str(t)
        # else:
        #     return expr[-1]
    if expr[0] != None:
        if type(expr[0]) != list and type(expr[0]) != STREE:
            if expr[0] in symbols and (is_method(expr[0], symbols) == False):
                return symbols[expr[0]]

            elif isinstance(expr[0], Method) and len(expr) == 1:
                # if expr[0].name == None:
                #     return evaluate(expr, symbols)
                return expr[0]

            elif is_method(expr[0], symbols):
                nsymbols = deepcopy(symbols)
                method = symbols[expr[0]]
                body = method.body
                args = method.args
                #print expr
                for index, arg in enumerate(args):
                    nsymbols[arg] = expr[index + 1]
                if method._parcount != None:
                    for k, v in method._parcount.items():
                        if k not in nsymbols:
                            nsymbols[k] = v

                #print nsymbols
                res = evaluate(body, nsymbols)
                #print "After", nsymbols
                for k, v in nsymbols.items():
                    if isinstance(v, Method):
                        v._parcount = nsymbols

                return res
                #return methods[expr[0]]
            elif type(expr[0]) == str and expr[0].startswith('@') and is_method(expr[0][1:], symbols):
                return symbols[expr[0][1:]]
            else:
                return expr[-1]
        else:
            return expr[-1]


symbols = {}
methods = {}
functions = {'+':operator('+'),
             '-':operator('-'),
             '/':operator('/'),
             '%':operator('%'),
             '*':operator('*'),
             '**':operator('**'),
             '=':operator('=='),
             '!=':operator('!='),
             'gt':operator('>'),
             'lt':operator('<'),
             '@!':psym(),
             "@":defsym(),
             "@F":deffun(methods),
             ":":qaccess(symbols, evaluate),
             ":/":qslice(symbols, evaluate),
             "#":qlen(symbols, evaluate),
             "unpack":unpack(symbols, evaluate_expr),
             "stdin":stdin,
             "stdout": stdout,
             }
string_except = {':', '#'}

def parse_line(line):
    p = Parser()
    return p.parse(line)



def set_rem(rem, symbols):

    if len(rem) <= 2:
        args = []
        #fbody = rem[1]
    else:
        #args = shlex.split(rem[1][1:-1])
        args = [rem[1].children[r].node for r in rem[1].children]

    #methods[rem[0].node] = [args, rem[-1]]
    symbols[rem[0].node] = Method(rem[0].node, rem[-1], args)
    return symbols[rem[0].node]


class Interpreter(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "limps> "
        self.intro = "Welcome to limps, My Lisp Implementation on Python"
    def do_exit(self, args):
       """Exits from the console"""
       return -1
    def do_EOF(self, args):
       """Exit on system end of file character"""
       return self.do_exit(args)

    def postloop(self):
       """Take care of any unfinished business.
          Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
       """
       cmd.Cmd.postloop(self)   ## Clean up command completion
       print "Bye!"

    def do_print(self, line):
       root = parse_line(line)
       root.print_tree()

    def do_load(self, line):
        with open(line) as f:
            root = parse_line(f.read())
            res = evaluate(root, symbols)
            print res

    def do_time(self, line):
        s = time()
        self.default(line)
        e = time()
        print e - s, "Seconds"

    def default(self, line):
       """Called on an input line when the command prefix is not recognized.
          In that case we execute the line as Python code.
       """
       root = parse_line(line)
       #root.print_tree()
       res = evaluate(root, symbols)
       print res



if __name__ == "__main__":

    if len(sys.argv) > 1:
        file_name = sys.argv[2]
        with open(file_name) as f:
            root = parse_line(f.read())
            if sys.argv[1] == "-F":
                res = evaluate(root, symbols)
                print res
            elif sys.argv[1] == "-P":
                root.print_tree()
    else:
        Interpreter().cmdloop()
