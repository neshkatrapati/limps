import graphviz as gv
import webbrowser

class STREE(object):
    node = None
    children = []
    def __init__(self, node, ntype="__meta__"):
        self.node = node
        self.children = {}
        self.type = ntype

    def print_tree(self):
        """
        Exposed function for printing the BST into graphviz and then showing through webbrowser.
        """
        graph = gv.Graph(format = 'svg')
        self._print_tree(graph)
        graph.render('img')
        webbrowser.open('img.svg')

    def _print_tree(self, graph, prefix = ""):
        """
        self.print_tree makes a graph and calls this function to recursively populate it.
        """

        data_as_string = prefix + "-" + str(self.node)  # graphviz cant take numbers
        graph.node(data_as_string) # Base case only one node
        print data_as_string, self.children
        #for index, child in enumerate(self.children):
        for index, child in self.children.items():
            child_data = str(child._print_tree(graph, prefix + str(index) + "." ))
            graph.edge(data_as_string, child_data)
        return data_as_string

    def flatten(self):
        s = ""
        if self.type == "__quote__":
            s += "`"
        elif self.type != "__meta__":
            s += self.node
        else:
            s = "<"

        t = []
        #print self.children.items()
        for index, child in sorted(self.children.items()):
            #print index
            if type(child) == STREE:
                t += [str(child.flatten())]
            else:
                t += [str(child)]

        s += " ".join(t)

        if self.type in  ["__meta__"]:
            s += ">"

        return s

    def __str__(self):
        if self.type != "__quote__":
            return self.node
        else:
            return self.flatten()

class Method(object):
    def __init__(self, name, body, args = []):
        self.name = name
        self.body = body
        self.args = args
        self._parcount = None

    def __str__(self):
        if self.name != None:
            return "Method : " + str(self.name)
        else:
            return "Anonymous Method"