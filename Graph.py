from collections import deque


class DAGError(Exception):

    """docstring for DAGError"""

    pass


class Vertex:

    """docstring for Vertex"""

    def __init__(self, node):
        self.node = node
        self.in_degree = None

    def __repr__(self):
        return "[" + repr(self.node) + ", " + repr(self.in_degree) + "]"

    def __str__(self):
        return repr(self.node)

    def __hash__(self):
        return hash(self.node)


class DAG:

    """docstring for Graph"""

    def __init__(self):
        self.graph = {}

    def __repr__(self):
        return repr(self.graph)

    def __str__(self):
        string_ = "DAG{\n"
        for v, edges in self.graph.items():
            string_ += "\t" + str(v) + ": {"
            fix_comma = False
            for e in edges:
                string_ += str(e) + ", "
                fix_comma = True
            if fix_comma:
                string_ = string_[:-2]
            string_ += "}\n"
        string_ += "   }\n"
        return string_

    # tests whether there is an edge from the vertices x to y
    def test_edge(self, x, y):
        if x in self.graph.keys():
            return y in self.graph[x]
        else:
            raise KeyError("vertex %s not in graph" % x)

    # lists all vertices y such that there is an edge from the vertices x to y
    def neighbors(self, x):
        if x in self.graph.keys():
            return self.graph[x]
        else:
            raise KeyError("vertex %s not in graph" % x)

    # adds the vertex x
    def add_vertex(self, vertex):
        if vertex in self.graph:
            raise KeyError("vertex %s already in graph" % vertex)
        elif not isinstance(vertex, Vertex):
            raise TypeError("vertex is not of type Vertex")
        else:
            self.graph[vertex] = set()

    # removes the vertex x
    def remove_vertex(self, vertex):
        if vertex not in self.graph:
            raise KeyError("vertex %s not in graph" % vertex)
        self.graph.pop(vertex)
        for edges in self.graph.values():
            if vertex in edges:
                edges.remove(vertex)

    # adds the edge from the vertices x to y
    def add_edge(self, x, y):
        if x in self.graph and y in self.graph:
            self.graph[x].add(y)
            if not self.is_valid():
                del self.graph[y]
                raise ValueError(
                    "adding edge %s -> %s creates a cycle" % (x, y))
        else:
            raise KeyError("vertex %s or %s not in graph" % (x, y))

    def remove_edge(self, x, y):
        if x in self.graph:
            if y in self.graph[x]:
                self.graph[x].remove(y)
            else:
                raise ValueError("no edge %s -> %s in graph" % (x, y))
        else:
            raise KeyError("vertex %s not in graph" % x)

    def is_valid(self):
        try:
            self.topological_ordering()
        except DAGError:
            return False
        return True

    def topological_ordering(self):
        """
        returns a list containing vertices in topological ordering
        raises DAGError if topological ordering cannot be found,
        i.e. graph has cycles.
        """
        ordered = []
        queue = deque()
        # find in-degree for each vertex
        for v in self.graph.keys():
            v.in_degree = 0
        for v in self.graph.keys():
            for u in self.graph[v]:
                u.in_degree += 1
        # add all vertices with no incoming edges to queue
        for v in self.graph.keys():
            if v.in_degree == 0:
                queue.append(v)
        # sort
        while len(queue) > 0:
            # pop a vertex with no incoming edges
            v = queue.pop()
            # add it to the topological ordering
            ordered.append(v)
            # decrement in-degree of all edges v -> u
            for u in self.graph[v]:
                u.in_degree += -1
                # if an edge has no more incoming edges, add it to our queue
                if u.in_degree == 0:
                    queue.append(u)

        if len(ordered) != len(self.graph):
            raise DAGError("Failed to find a topological ordering.")

        return ordered


def __test_DAG(crash=False):
    """test Graph class, return True if test successful"""

    def test_vertex(crash):
        try:
            v = Vertex('A')
            str(v)
            repr(v)
            hash(v)
            return True

        except Exception as e:
            if crash:
                raise e
            return False

    def test_add_vertex(crash):
        try:
            vertices = [
                Vertex('A'),
                Vertex('B'),
                Vertex('C'),
                Vertex('D'),
                Vertex('E')]
            g = DAG()
            for v in vertices:
                g.add_vertex(v)

            if len(g.graph) != 5:
                raise Exception("failed to add all vertices to graph")
            return True

        except Exception as e:
            if crash:
                print("graph: \n" + str(g))
                raise e
            return False

    def test_remove_vertex(crash):
        try:
            vertices = [Vertex('A'),
                        Vertex('B'),
                        Vertex('C'),
                        Vertex('D'),
                        Vertex('E')]
            g = DAG()
            for v in vertices:
                g.add_vertex(v)
            g.add_edge(vertices[1], vertices[2])
            g.add_edge(vertices[3], vertices[0])
            g.remove_vertex(vertices[2])
            for v, edges in g.graph.items():
                if vertices[2] is v or vertices[2] in edges:
                    raise Exception(
                        "failed to fully delete vertex %s from graph"
                        % vertices[2])
            return True

        except Exception as e:
            if crash:
                print("graph: \n" + str(g))
                raise e
            return False

    def test_add_edge(crash):
        try:
            vertices = [Vertex('A'),
                        Vertex('B'),
                        Vertex('C'),
                        Vertex('D'),
                        Vertex('E')]
            g = DAG()
            for v in vertices:
                g.add_vertex(v)
            g.add_edge(vertices[1], vertices[2])
            g.add_edge(vertices[3], vertices[0])
            return True

        except Exception as e:
            if crash:
                raise e
            return False

    def test_remove_edge(crash):
        try:
            return True
        except Exception as e:
            if crash:
                raise e
            return False

    test = ""
    if test_vertex(crash):
        test += '+'
    else:
        test += '-'
    if test_add_vertex(crash):
        test += '+'
    else:
        test += '-'
    if test_remove_vertex(crash):
        test += '+'
    else:
        test += '-'
    if test_add_edge(crash):
        test += '+'
    else:
        test += '-'
    if test_remove_edge(crash):
        test += '+'
    else:
        test += '-'
    return test

if __name__ == "__main__":
    print(__test_DAG(crash=True))
