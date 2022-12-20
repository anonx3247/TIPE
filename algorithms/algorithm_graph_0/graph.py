# for graph operations
import numpy as np
import osmnx as ox
from matplotlib import pyplot as plt

# for animation
from matplotlib.animation import FuncAnimation as fn_anim

# for djikstra algorithm
from heapq import *
from math import inf

# for file operations
from os.path import exists

class Graph:
    """
    Un Graphe est un objet enregistrant a la fois le graphe osmnx
    ainsi qu'une forme plus exploitable, notamment avec des neouds indices de 0
    a n et muni d'une matrice d'adjacence, et de nombreuses methodes pour faciliter
    son exploitation
    """
    def __init__(self, G=None, place=None, address=None, name=None):
        assert(G != None or address != None or place != None or name != None)
        if name != None and exists(name + ".gml"):
            G = ox.load_graphml(name+".gml")
        else:
            if G == None and address != None and place == None:
                G = ox.graph_from_address(address)
                ox.save_graphml(G, name+".gml")
            elif G == None and address == None and place != None:
                G = ox.graph_from_place(place)
                ox.save_graphml(G, name+".gml")
            elif G == None and address == None and place == None:
                G = ox.load_graphml(name+".gml")
        
        members = [i for i in G.nodes]
        n = G.order()
        adj = np.zeros((n, n))

        orig_adj = [i for i in G.adjacency()]
        for i in range(n):
            successors = [j for j in G.successors(members[i])]
            for j in range(n):
                if members[j] in successors:
                    adj[i, j] = orig_adj[i][1][members[j]][0]["length"]

        self.name = name
        self.members = members
        self.adj = adj
        self.rep = ox.plot_graph(G, save=True, filepath=name+".png")
        self.size = len(members)
        self.graph = G
        self.dists_from = {}

    def deg(self, i: int) -> int:
        """
        renvoie le degre d'un point
        """
        d = 0
        for j in range(self.size):
            if self.adj[i, j] != 0:
                d += 1
        return d

    def links(self, pt: int, n: int) -> list:
        """
        renvoie les noeuds a n degres de parente de pt
        """
        if n == 0:
            return []
        S = []
        L = []
        for i in range(self.size):
            if self.adj[pt, i] != 0:
                L.append(i)
        S += L
        for i in L:
            S += self.links(i, n - 1)
        return S

    def deginf(self, pt: int, lev: int) -> int:
        """
        donne le degré infini (évalué a n niveaux de parenté) de chaque point
        """
        degG = self.deg(pt)
        if lev == 0:
            return degG
        deginfG = degG  # liste des deginf des pts de G
        for j in self.links(pt, lev):
            deginfG += self.deginf(j, lev - 1)
        return deginfG

    def plot_node(self, i: int):
        """
        affiche le noeud sur l'image du graphe
        """
        bkg = ox.plot_graph(self.graph, show=False)
        x, y = self.coordinates(pt=i)
        plt.scatter([x], [y], color='blue')

    def plot_nodes(self, L: list):
        """
        affiche les noeuds sur l'image du graphe
        """
        coords = self.coordinates(pts=L)
        x = [i[0] for i in coords]
        y = [i[1] for i in coords]
        bkg = ox.plot_graph(self.graph, show=False)
        plt.plot(x, y, color = 'green')

    def plot_path(self, path: list):
        """
        affiche les noeuds sur l'image du graphe
        """
        coords = self.coordinates(pts=path)
        x = [i[0] for i in coords]
        y = [i[1] for i in coords]
        bkg = ox.plot_graph(self.graph, show=False)
        plt.plot(x, y,
                color = 'red',
                linestyle = 'solid',
                marker = 'o')

    def plot_neighbors(self, i: int, n: int):
        """
        montre les voisins sur l'image, a n degres de parente
        """
        L = self.links(i, n)
        self.plot_nodes(L)

    def plot(self) -> plt.plot:
        return ox.plot_graph(self.graph, show=False)

    def coordinates(self, pt: int = None, pts: list = None) -> tuple:
        assert(pt != None or pts != None)
        if pt == None:
            return [self.coordinates(pt=i) for i in pts]
        else:
            id = self.members[pt]
            x = self.graph.nodes[id]['x']
            y = self.graph.nodes[id]['y']
            return x,y

    def djikstra(self, sommet: int, animate=False) -> list:
        """
        algorithme de recherche des chemins les plus courts
        """
        if animate:
            x, y = [], []
            vus = [[]]

        if sommet in self.dists_from:
            return self.dists_from[sommet]
        distances = [(inf, i, None) for i in range(self.size)]
        distances[sommet] = (0, sommet, sommet)
        heap = []
        for i in range(self.size):
            heappush(heap, distances[i])
        non_vus = [True for i in self.adj]
        sommet_actuel = sommet
        dist_actuelle = 0

        while True in non_vus:
            dist_actuelle, sommet_actuel, origine = heappop(heap)
            if animate:
                xi, yi = self.coordinates(sommet_actuel)
                vus.append([self.coordinates(i) for i in range(len(non_vus)) if not non_vus[i]])
                x.append(xi)
                y.append(yi)
            if dist_actuelle == inf:
                break
            distances[sommet_actuel] = (dist_actuelle, sommet_actuel, origine)
            voisins = self.voisins_a_traiter(sommet_actuel, non_vus)
            for voisin in voisins:
                heappush(heap, (dist_actuelle + self.adj[sommet_actuel,voisin], voisin, sommet_actuel))
            non_vus[sommet_actuel] = False

        self.dists_from[sommet] = distances
        
        if animate:
            fig, ax = plt.subplots()

            vus_x = [ [x for (x,y) in i] for i in vus]
            vus_y = [ [y for (x,y) in i] for i in vus]

            bkg = ox.plot_graph(self.graph, ax=ax, show=False)

            step = 50

            animation = fn_anim(fig,
                        func = self.djikstra_anim,
                        fargs = (x, y, ax, vus_x, vus_y, step),
                        frames = np.arange(0, len(x)//step, 1),
                        interval = 0.0001)
            plt.show()
        return distances

    def djikstra_anim(self, i, x, y, ax, vus_x, vus_y, step):
                assert(i*step <= len(x))
                ax.scatter(vus_x[i*step], vus_y[i*step], color='blue')
                ax.scatter(x[max(0, i*step-step):i*step], y[max(0, i*step-step):i*step], color="red")
        

    def voisins_a_traiter(self, sommet: int, non_vus: list) -> list:
        v = []
        for i in range(self.size):
            if self.adj[sommet,i] != 0 and non_vus[i] and i != sommet:
                v.append(i)
        return v

    def dist(self, i: int, j: int) -> float:
        """
        returns distance between i and j 
        """
        return self.djikstra(i)[j][0]

    def chemin(self, i: int, j: int, show=False) -> (float, list):
        """
        renvoie le chemin le plus court de i a j
        et la distance de ce parcours
        """
        if not i in self.dists_from:
            self.djikstra(i)
        if self.dists_from[i][j][0] == inf:
            return (inf, [])
        else:
            actuel = j
            c = [j]
            while actuel != i:
                c.append(self.dists_from[i][actuel][2])
                actuel = self.dists_from[i][actuel][2]
            if show:
                self.plot_path(c)
            else:
                return (self.dists_from[i][j][0], c)

    def etendue_minimale_moyenne(self) -> float:
        """
        Renovoie la distance minimle entre deux points moyenne
        """
        M = Stats([])
        for i in range(self.size):
            dists = []
            for j in self.links(i, 1):
                dists.append(self.adj[i, j])
            if dists != []:
                M.append(min(dists))
        return M.avg()

class Stats:
    """
    classe d'utilitaires pour listes, pour effectuer des statistiques
    """
    def __init__(self, L: list):
        self.data = L
        self.size = len(L)
        self.sorted = sorted(L)

    def sum(self):
        S = 0
        for i in self.data:
            S += i
        return S

    def avg(self):
        return self.sum()/self.size


    def q1(self):
        return self.get_median(self.sorted[:self.size // 2])


    def q3(self):
        return self.get_median(self.sorted[self.size // 2:])

    def median(self):
        return self.sorted[self.size // 2]

    def append(self, elem):
        self.data.append(elem)
        self.size += 1

    def get_median(self, lst):
        """
        suppose une lst triee
        """
        return lst[len(lst) // 2]

    def stats(self):
        print("Data:", self.data[:min([10, self.size])])
        print("Average:", self.avg())
        print("Q1:", self.q1())
        print("Median:", self.median())
        print("Q3:", self.q3())

