from stree import *
import shlex
BRACE_OPEN = '<'
BRACE_CLOSE = '>'
#by_space = re.compile("\s+")
#by_space = re.compile(r'''((?:[^\s+"']|"[^"]*"|'[^']*')+)''')

class Parser(object):
    def parse(self,line):
        root = STREE("__root__")
        current = root
        stack = []
        total_nodes = 1
        buf = ""
        bufstack  = []
        for index, char in enumerate(line):
            if char == BRACE_OPEN:
                new = STREE("child_"+str(total_nodes))
                comps = shlex.split(buf)
                comp_len = len(comps) + len(current.children)
                current.children[comp_len] = new
                total_nodes += 1
                stack.append(current)
                bufstack.append(buf)
                buf = ""
                current = new
            elif char == BRACE_CLOSE:
                if len(buf) > 0:
                    comps = shlex.split(buf)
                    comp_len = len(comps)
                    c = 0
                    i = 0
                    while i < comp_len:
                        if c not in current.children:
                            next_element = STREE(comps[i], "__atom__")
                            current.children[c] = next_element
                            i += 1
                        c += 1
                    if len(bufstack) > 0:
                        buf = bufstack.pop()
                    else:
                        buf = []
                current = stack.pop()
            else:
                buf += char
        return root
