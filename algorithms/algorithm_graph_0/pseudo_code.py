# Pseudo-code for graph algorithm

# let G be our oriented Graph, and A be the Adjacency Matrix

class Point:
	self.name
	self.deg
	self.deg_inf
	
	def __init__(name):
		self.name = name

class Graph:
	self.points = []
	self.adj = {}
	self.avg_deg = 0
	self.avg_high_deg = 0

	def __init__(pts: list[Point], A: dict, N: int) -> Graph:
		"""Genere les valeurs et construit le graphe"""
		self.adj = A
		self.points = [Point(i) for i in pts]
		self.set_degrees(N)
		self.avg_deg = self.avg_deg()
		self.avg_high_deg = avg_high_deg()

	# Calculating Stats
	def deg(i: Point) -> int:
		"""Trouve le degre d'un point i dans G"""
		d = 0
		for j in self.points:
			if G.adj[i][j] != 0:
				d += 1
		return d
		
	def adjacents(i: Point) -> list:
		return [i for i in self.adj[i].keys()]

	def degN(i: Point, N: int) -> int:
		"""Calclue le degre de rang N du ppint i dans G
		N doit etre superieur a 1"""
		d = i.deg
		if N = 1:
			return d
		else:
			for j in self.adjacents(i):
				d += degN(j, N-1)
			return d

	def set_degrees(N: int):
		"""assigne deg, et deg_inf a tous les points du Graphe"""
		for point in self.points:
			point.deg = deg(point)
		for point in self.points:
			point.deg_inf = degN(point, N)
	
	def avg_deg():
		S = 0
		for i in self.points:
			S += i.deg_inf
		return S/len(self.points)
	
	def avg_high_deg():
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
		
	G = Graph(pts, A, 3)
	print("Points:", G.points)
	print("Point 0:", G.points[0].name)
	print(G.points[0].deg, G.points[0].deg_inf)
			
			
