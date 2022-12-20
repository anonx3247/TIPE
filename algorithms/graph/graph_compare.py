# for graph operations
import numpy as np
import osmnx as ox
from matplotlib import pyplot as plt

# for animation
from matplotlib.animation import FuncAnimation as fn_anim

# for djikstra and A* algorithm
from heapq import *
from math import inf, sqrt

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
        adj = self.initialize_adj(n)

        orig_adj = [i for i in G.adjacency()]
        for i in range(n):
            successors = [j for j in G.successors(members[i])]
            for j in range(n):
                if members[j] in successors:
                    adj[i, j] = orig_adj[i][1][members[j]][0]["length"]

        self.anim_finished = False
        self.name = name
        self.members = members
        self.adj = adj
        self.rep = ox.plot_graph(G, save=True, filepath=name+".png")
        self.size = len(members)
        self.graph = G
        self.dists_from = {}
        self.chemins = {}


    def deg(self, i: int) -> int:
        """
        renvoie le degre d'un point
        """
        d = 0
        for j in range(self.size):
            if self.connected(i,j):
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
            if self.connected(pt, i):
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

    def djikstra(self, sommet: int, animate=False, save=False) -> list:
        """
        algorithme de recherche des chemins les plus courts
        """
        if save:
            assert(animate)
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

            step = self.size//100

            animation = fn_anim(fig,
                        func = self.djikstra_anim,
                        fargs = (x, y, ax, vus_x, vus_y, step),
                        frames = np.arange(0, len(x)//step, 1),
                        interval = 0.0001,
                        repeat = False)
            if save:
                animation.save('djikstra_' + self.name + '_' + str(sommet) + '.mp4', 
                                writer='ffmpeg')
            else:
                plt.show()
        return distances

    def euclidean_dist(self, i: int, j: int):
        x1, y1 = self.coordinates(i)
        x2, y2 = self.coordinates(j)
        return sqrt(
            (x2-x1)**2 + (y2-y1)**2
        )

    def A_star(self, debut: int, fin: int, animate=False, save=False) -> list:
        """
        algorithme de recherche des chemins les plus courts
        """
        if save:
            assert(animate)
        if animate:
            x, y = [], []
            vus = [[]]

        if (debut, fin) in self.chemins:
            return self.chemins[(debut, fin)]
        distances = [(inf, i, None) for i in range(self.size)]
        distances[debut] = (self.euclidean_dist(debut, fin), 0, debut)
        heap = []
        for i in range(self.size):
            heappush(heap, distances[i])
        non_vus = [True for i in self.adj]
        sommet_actuel = debut
        dist_possible = self.euclidean_dist(debut, fin)
        dist_actuelle = 0
        ancetres = [i for i in range(self.size)]
        ancetres[debut] = None

        while True in non_vus:
            dist_possible, dist_actuelle, sommet_actuel = heappop(heap)
            origine = ancetres[sommet_actuel]
            if animate:
                xi, yi = self.coordinates(sommet_actuel)
                vus.append([self.coordinates(i) for i in range(len(non_vus)) if not non_vus[i]])
                x.append(xi)
                y.append(yi)
            if sommet_actuel == fin:
                break
            distances[sommet_actuel] = (dist_possible, dist_actuelle, sommet_actuel)
            voisins = self.voisins_a_traiter(sommet_actuel, non_vus)
            for voisin in voisins:
                heappush(heap, (dist_actuelle + self.adj[sommet_actuel,voisin] + self.euclidean_dist(sommet_actuel, fin), 
                                dist_actuelle,
                                voisin))
                ancetres[voisin] = sommet_actuel
            non_vus[sommet_actuel] = False

        path = self.reconstitue_chemin(ancetres, fin)
        
        if animate:
            fig, ax = plt.subplots()

            vus_x = [ [x for (x,y) in i] for i in vus]
            vus_y = [ [y for (x,y) in i] for i in vus]

            bkg = ox.plot_graph(self.graph, ax=ax, show=False)

            step = self.size//100

            animation = fn_anim(fig,
                        func = self.A_anim,
                        fargs = (x, y, ax, vus_x, vus_y, step, path),
                        frames = np.arange(0, len(x)//step + step, 1),
                        interval = 200,
                        repeat = False)
            if save:
                animation.save('A_star_' + self.name + '_' + str(debut) + '_' + str(fin) + '.mp4', 
                                writer='ffmpeg')
            else:
                plt.show()
            self.anim_finished = False
        
        self.chemins[(debut, fin)] = path
        return distances[fin][1], path

    def reconstitue_chemin(self, ancetres, fin):
        i = fin
        chemin = [i]
        while ancetres[i] != None:
            chemin.append(ancetres[i])
            i = ancetres[i]
        chemin.reverse()
        return chemin

    def djikstra_anim(self, i, x, y, ax, vus_x, vus_y, step):
        if (i+1)*step > len(x):
            self.anim_finished = True
        if not self.anim_finished:
            ax.scatter(vus_x[i*step], vus_y[i*step], color='blue')
            ax.scatter(x[max(0, i*step-step):i*step], y[max(0, i*step-step):i*step], color="red")

    def A_anim(self, i, x, y, ax, vus_x, vus_y, step, path):
        if i <= len(x)//step:
            ax.scatter(vus_x[i*step], vus_y[i*step], color='blue')
            ax.scatter(x[max(0, i*step-step):i*step], y[max(0, i*step-step):i*step], color="red")
        else:
            x = [self.coordinates(i)[0] for i in path]
            y = [self.coordinates(i)[1] for i in path]
            ax.plot(x, y, color='red')
        

    def voisins_a_traiter(self, sommet: int, non_vus: list) -> list:
        v = []
        for i in range(self.size):
            if self.connected(sommet, i) and non_vus[i] and i != sommet:
                v.append(i)
        return v

    def dist(self, i: int, j: int) -> float:
        """
        returns distance between i and j 
        """
        return self.A_star(i)[j][0]

    def chemin(self, i: int, j: int, show=False) -> (float, list):
        """
        renvoie le chemin le plus court de i a j
        et la distance de ce parcours
        """
        c = self.A_star(i,j)
        if show:
            self.plot_path(c)
            plt.show()
        return c

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


class SmallGraph(Graph):
    def initialize_adj(self, n: int):
        return np.zeros((n,n))

    def connected(self, i: int, j: int) -> bool:
        return self.adj[i,j] != 0

class BigGraph(Graph):
    def initialize_adj(self, n: int):
        return {}

    def connected(self, i: int, j: int) -> bool:
        return (i,j) in self.adj

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
