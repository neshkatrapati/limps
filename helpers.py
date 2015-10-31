from stree import *
def is_method(m, symbols):
    if (m in symbols) and isinstance(symbols[m], Method):
        return True
    return False

def convert_to_bool(val):
    if val == "True":
        return True
    return False
