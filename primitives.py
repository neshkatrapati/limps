



def operator(op):
    def _eval(arglist):
        return eval(op.join(arglist))
    return _eval

def defsym(symbols):
    def _eval(arglist):
        symbols[arglist[0]] = arglist[1]
        return str(arglist[0]) + "=" + str(arglist[1])
    return _eval

def psym(symbols):
    def _eval(arglist):
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


