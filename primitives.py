
from stree import *
from copy import deepcopy

def operator(op):
    def _eval(arglist):
        # print arglist
        if type(arglist[0]) != STREE and type(arglist[1]) != STREE:
            #print arglist
            return eval(op.join(arglist))
        else:
            #print arglist
            if type(arglist[0]) == STREE:
                l = list_add(arglist[0], arglist[1])
            elif type(arglist[1]) == STREE:
                l = list_add(arglist[1], arglist[0], True)

            if len(arglist) > 2:

                for el in arglist[2:]:
                    l = list_add(l, el)
            return l
    return _eval


def list_add(l, el, rev = False):
    m = Method(None, l.children[0])
    elements = deepcopy(m.body.children)
    elid = 0
    if len(elements.keys()) > 0:
        if rev == False:
            elid = max(elements.keys()) + 1
        else:
            #print "Test"
            elid = min(elements.keys()) - 1
            #print elid
    if type(el) in [STREE, Method]:
        #print type(el)
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

def limps_string(string):
    return "\"" + string  + "\""

def stringify(args):
    if '\"' in args[0]:
        args[0] = args[0].replace('\"', '')

    return limps_string(args[0])

def get_type(symbols):
    def _eval(args):
        #print args
        if type(args[0]) == STREE:
            return limps_string("composite")
        elif type(args[0]) == Method or ((args[0] in symbols) and type(symbols[args[0]]) == Method):
            return limps_string("method")
        else:
            return limps_string("atomic")
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
        #arglist[0] = arglist[0].nam
        if type(arglist[0]) == STREE:
            #print arglist
            m = Method(None, arglist[0].children[0])
            elements = m.body.children
            key = elements.keys()[0]
            return evaluate(m.body, symbols)
        #return evaluate(arglist, symbols)
    return _eval


def qaccess(symbols, evaluate):
    def _eval(arglist):
        #print arglist
        index = int(arglist[-1])

        if type(arglist[0]) == STREE:

            m = Method(None, arglist[0].children[0])
            elements = m.body.children
            key = elements.keys()[index]
            x = elements[key]
            #print type(x)
            return x
        else:
            #print arglist
            return arglist[0][index]
    return _eval

def make_list(l= []):
    s = STREE(None, ntype = '__quote__')
    sm = STREE(None, ntype = '__meta__')
    for index, key in enumerate(l):
        sm.children[index] = key
    s.children[0] = sm
    return s


def qslice(symbols, evaluate):
    def _eval(arglist):
        f, t = int(arglist[-2]), int(arglist[-1])
        if type(arglist[0]) == STREE:
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
        else:
            return arglist[0][f:t]
    return _eval

def qlen(symbols, evaluate):
    def _eval(arglist):
        if type(arglist[0]) == STREE:
            m = Method(None, arglist[0].children[0])
            elements = m.body.children
            return len(elements)

        else:
            return len(arglist[0])
    return _eval