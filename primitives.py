
from stree import *


def operator(op):
    def _eval(arglist):
        #print arglist
        return eval(op.join(arglist))
    return _eval

def defsym():
    def _eval(arglist, symbols):
        symbols[arglist[0]] = arglist[1]
        return str(arglist[0]) + "=" + str(arglist[1])
    return _eval

def psym():
    def _eval(arglist, symbols):
        import pprint
        pprint.pprint(symbols)
    return _eval

def deffun(methods):
    def _eval(arglist):
        methods[arglist[0]] = arglist[1]
        #return str(arglist[0]) + "=" + str(arglist[1])
    return _eval


def stdin(string):
    return raw_input(string[0])

def stdout(arglist):
    for arg in arglist:
        print arg,
    print ""

def unpack(symbols, evaluate):
    def _eval(arglist):
        arglist[0] = arglist[0].name
        #print arglist
        return evaluate(arglist, symbols)
    return _eval


def qaccess(symbols, evaluate):
    def _eval(arglist):
        index = int(arglist[-1])
        m = Method(None, arglist[0].children[0])
        elements = m.body.children
        key = elements.keys()[index]
        x = elements[key]
        return x
    return _eval

def qslice(symbols, evaluate):
    def _eval(arglist):
        f, t = int(arglist[-2]), int(arglist[-1])
        m = Method(None, arglist[0].children[0])
        elements = m.body.children
        keys = elements.keys()[f:t+1]
        s = STREE(None, ntype = '__quote__')
        sm = STREE(None, ntype = '__meta__')
        for index, key in enumerate(keys):
            x = elements[key]
            sm.children[index] = x
        s.children[0] = sm
        return s
    return _eval

def qlen(symbols, evaluate):
    def _eval(arglist):
        m = Method(None, arglist[0].children[0])
        elements = m.body.children
        return len(elements)

    return _eval