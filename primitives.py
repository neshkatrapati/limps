
from stree import *
from copy import deepcopy

def operator(op):
    def _eval(arglist):
        #print arglist
        if type(arglist[0]) != STREE:
            return eval(op.join(arglist))
        else:

            return list_add(arglist[0], arglist[1])
    return _eval

def list_add(l, el):
    m = Method(None, l.children[0])
    elements = deepcopy(m.body.children)
    elid = 0
    if len(elements.keys()) > 0:
        elid = max(elements.keys()) + 1
    if type(el)  == STREE:
        nc = el
    else:
        nc = STREE(el, '__atom__')

   # print el, nc.type

    elements[elid] = nc
    s = STREE(None, '__quote__')
    sm = STREE(None, '__meta__')
    sm.children = elements
    s.children[0] = sm
    #print sm.children
    return s

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
        #print arglist
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