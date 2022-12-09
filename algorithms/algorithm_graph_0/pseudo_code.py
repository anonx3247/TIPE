# Pseudo-code for graph algorithm

# let G be our oriented Graph, and A be the Adjacency Matrix

class Point:
    name = ""
    deg = 0
    deg_inf = 0

    def __init__(self, name):
        self.name = name


class Graph:
    points = []
    adj = {}
    avg_deg = 0
    avg_high_deg = 0

    def __init__(self, A: dict, N: int):
        """Genere les valeurs et construit le graphe"""
        self.adj = self.conv_to_pts(A)
        self.points = [pt for pt in self.adj.keys()]
        self.set_degrees(N)
        self.avg_deg = self.avg_deg()
        self.avg_high_deg = self.avg_high_deg()

    def conv_to_pts(self, A: dict):
        """Construit un dictionaire d'adjacence avec des points comme clefs
        et non pas des str"""
        B = {}
        for i in A.keys():
            for j in A[i].keys():
                B[Point(i)] = Point(j)
        return B

    def _adj(self, i: Point, j: Point) -> float:
        return self.adj[i.name][j.name]

    # Calculating Stats
    def deg(self, i: Point) -> int:
        """Trouve le degre d'un point i dans G"""
        return len(self.adjacents(i))

    def adjacents(self, i: Point) -> list:
        return [i for i in self.adj[i.name].keys()]

    def degN(self, i: Point, N: int) -> int:
        """Calclue le degre de rang N du ppint i dans G
        N doit etre superieur a 1"""
        d = i.deg
        if N == 1:
            return d
        else:
            for j in self.adjacents(i):
                d += self.degN(j, N-1)
        return d

    def set_degrees(self, N: int):
        """assigne deg, et deg_inf a tous les points du Graphe"""
        for point in self.points:
            point.deg = self.deg(point)
        for point in self.points:
            point.deg_inf = self.degN(point, N)

    def avg_deg(self):
        S = 0
        for i in self.points:
            S += i.deg_inf
        return S/len(self.points)

    def avg_high_deg(self):
        degrees = [i.deg for i in self.points]
        degrees.sort()
        med = degrees[len(degrees)//2]
        high = degrees[med:]
        return high[len(high)//2]

# Lets test witsh an example:


def test():
    pts = ["A", "B", "C", "D", "E", "F"]
    A = { "A": {"F": 5},
    "B": {"C": 7},
    "C": {"B": 7, "D": 2},
    "D": {"C": 2},
    "E": {"C": 6, "D": 1}}

    G = Graph(A, 3)
    print("Points:", G.points)
    print("Point 0:", G.points[0].name)
    print(G.points[0].deg, G.points[0].deg_inf)
