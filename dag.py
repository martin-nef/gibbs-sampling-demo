from collections import deque


class DAGError(Exception):

    """docstring for DAGError"""

    pass


class Vertex(str):

    """docstring for Vertex"""

    def __init__(self, node):
        self.node = node
        self.in_degree = None


class DAG:

    """docstring for Graph"""

    def __init__(self):
        self.graph = {}

    def __repr__(self):
        return repr(self.graph)

    def __str__(self):
        string_ = "{\n"
        for v, edges in self.graph.items():
            string_ += "\t" + str(v) + ": {"
            fix_comma = False
            for e in edges:
                string_ += str(e) + ", "
                fix_comma = True
            if fix_comma:
                string_ = string_[:-2]
            string_ += "}\n"
        string_ += "}\n"
        return string_

    # tests whether there is an edge from the vertices x to y
    def test_edge(self, x, y):
        if x in self.graph:
            return y in self.graph[x]
        else:
            raise KeyError("vertex %s not in graph" % x)

    # lists all vertices y such that there is an edge from the verticex x to y
    def neighbors(self, x):
        if x in self.graph:
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

    # adds the edge from vertex x to y
    def add_edge(self, x, y):
        if x in self.graph and y in self.graph:
            self.graph[x].add(y)
            if not self.is_valid():
                del self.graph[y]
                raise ValueError(
                    "adding edge %s -> %s creates a cycle" % (x, y))
        else:
            raise KeyError("vertex %s or %s not in graph" % (x, y))

    # remove edge from vertex x to y
    def remove_edge(self, x, y):
        if x in self.graph:
            if y in self.graph[x]:
                self.graph[x].remove(y)
            else:
                raise ValueError("no edge %s -> %s in graph" % (x, y))
        else:
            raise KeyError("vertex %s not in graph" % x)

    def is_valid(self):
        """
        returns a list containing vertices in topological ordering
        raises DAGError if topological ordering cannot be found,
        i.e. graph has cycles.
        """
        nodes_visited = 0
        queue = deque()
        # find in-degree for each vertex
        for v in self.graph:
            v.in_degree = 0
        for v in self.graph:
            for u in self.graph[v]:
                u.in_degree += 1
        # add all vertices with no incoming edges to queue
        for v in self.graph:
            if v.in_degree == 0:
                queue.append(v)
        # sort
        while len(queue) > 0:
            # pop a vertex with no incoming edges
            v = queue.pop()
            # increment nodes visited
            nodes_visited += 1
            # quit the loop if we visited more nodes than there are in the
            # graph
            if nodes_visited > len(self.graph):
                break
            # decrement in-degree of all edges v -> u
            for u in self.graph[v]:
                u.in_degree += -1
                # if an edge has no more incoming edges, add it to our queue
                if u.in_degree == 0:
                    queue.append(u)

        return nodes_visited == len(self.graph)


def __test_DAG(crash=False):
    """
    test Graph class, return set of
    characters representing success of each test
    """

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
        test1 = False
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

            test1 = True
            if len(g.graph) != 5:
                if crash:
                    raise Exception("failed to add all vertices to graph")
                test1 = False

        except Exception as e:
            if crash:
                print("graph: \n" + str(g))
                raise e
            test1 = False

        test2 = False
        try:
            g = DAG()
            g.add_vertex(Vertex('A'))
            g.add_vertex(Vertex('A'))
            test2 = False
        except KeyError:
            test2 = True

        return test1 and test2

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
            g = DAG()
            a = Vertex('A')
            b = Vertex('B')
            g.add_vertex(a)
            g.add_vertex(b)
            g.add_edge(a, b)
            if b not in g.graph[a]:
                return False
        except Exception as e:
            if crash:
                raise e
            return False
        return True

    def test_remove_edge(crash):
        try:
            g = DAG()
            a = Vertex('A')
            b = Vertex('B')
            g.add_vertex(a)
            g.add_vertex(b)
            g.add_edge(a, b)
            g.remove_edge(a, b)
            if b in g.graph[a]:
                return False
        except Exception as e:
            if crash:
                raise e
            return False
        return True

    def test_is_valid(crash):

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
        g.graph[vertices[2]].add(vertices[1])
        if g.is_valid():
            if crash:
                raise DAGError("Cycle not detected.")
            return False
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
        g.add_edge(vertices[3], vertices[2])
        if not g.is_valid():
            return False
        return True

    failed_tests = []
    test = ""
    if test_vertex(crash):
        test += '+'
    else:
        test += '-'
        failed_tests.append("vertex")
    if test_add_vertex(crash):
        test += '+'
    else:
        test += '-'
        failed_tests.append("add_vertex")
    if test_remove_vertex(crash):
        test += '+'
    else:
        test += '-'
        failed_tests.append("remove_vertex")
    if test_add_edge(crash):
        test += '+'
    else:
        test += '-'
        failed_tests.append("add_edge")
    if test_remove_edge(crash):
        test += '+'
    else:
        test += '-'
        failed_tests.append("remove_edge")
    if test_is_valid(crash):
        test += '+'
    else:
        test += '-'
        failed_tests.append("is_valid")
    if failed_tests:
        test += "\nfailed tests: "
        for failed_test in failed_tests:
            test += failed_test + ", "
        test = test[0:len(test) - 2]
    return test


if __name__ == "__main__":
    test_results = __test_DAG(True)
    if test_results == "++++++":
        print("All tests passed")
    else:
        print(test_results.replace("+", "").replace("-", "").replace("\n", "", 1))
