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
        quoteBef = False
        bufstack  = []
        for index, char in enumerate(line):
            if char == BRACE_OPEN:

                new = STREE("child_"+str(total_nodes))
                comps = shlex.split(buf)
                comp_len = len(comps) + len(current.children)

                if quoteBef:
                    par = STREE("child_"+str(total_nodes)+'_quote', "__quote__")
                    par.children[0] = new
                    current.children[comp_len] = par
                else:
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

                            if ((i + 1) not in current.children) or current.children[i + 1].type != '__quote__':
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
                if quoteBef:
                    quoteBef = False
                if char == "`":
                    quoteBef = True
                buf += char
        return root

