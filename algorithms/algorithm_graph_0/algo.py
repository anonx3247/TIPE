# from matlpotlib import pyplot as plt
import numpy as np
import osmnx as ox
from heapq import *
from math import inf
import matplotlib.pyplot as plt

# G = ox.graph_from_place("Saint Germain en Laye, France")
H = ox.graph_from_address("1 Venelle Artémis, Saint Germain en Laye, france")

# Soit Adj la matrice d'adjacence

n = 0  # taille du graph
Adj = np.zeros((n, n))  # Avec A[i][j] la distance entre i et j, qui peut etre
# None si i et j ne sont pas reliés


class Graph:
    def __init__(self, G):
        members = [i for i in G.nodes]
        n = G.order()
        adj = np.zeros((n, n))

        orig_adj = [i for i in G.adjacency()]
        for i in range(n):
            successors = [j for j in G.successors(members[i])]
            for j in range(n):
                if members[j] in successors:
                    adj[i, j] = orig_adj[i][1][members[j]][0]["length"]

        self.members = members
        self.adj = adj
        self.rep = ox.plot_graph(G)
        self.size = len(members)
        self.graph = G

    def deg(self, i: int) -> int:
        d = 0
        for j in range(self.size):
            if self.adj[i, j] != 0:
                d += 1
        return d

    def links(self, pt: int, n: int) -> list:
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
        degG = self.deg(pt)
        if lev == 0:
            return degG
        deginfG = degG  # liste des deginf des pts de G
        for j in self.links(pt, lev):
            deginfG += self.deginf(j, lev - 1)
        return deginfG

    def show_node(self, i: int) -> plt.plot:
        return ox.plot_graph_route(self.graph, [self.members[i]])

    def show_nodes(self, L: list) -> plt.plot:
        lst = [self.members[i] for i in L]
        return ox.plot_graph_route(self.graph, lst)

    def show_neighbors(self, i: int, n: int) -> plt.plot:
        L = self.links(i, n)
        lst = [self.members[j] for j in L]
        return ox.plot_graph_routes(self.graph, [[self.members[i]], lst])

    def djikstra(self, sommet):
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
            if dist_actuelle == inf:
                break
            distances[sommet_actuel] = (dist_actuelle, sommet_actuel, origine)
            voisins = self.voisins_a_traiter(sommet_actuel, non_vus)
            for voisin in voisins:
                heappush(heap, (dist_actuelle + self.adj[sommet_actuel,voisin], voisin, sommet_actuel))
            non_vus[sommet_actuel] = False

        return distances

    def voisins_a_traiter(self, sommet, non_vus):
        v = []
        for i in range(self.size):
            if self.adj[sommet,i] != 0 and non_vus[i]:
                v.append(i)
        return v

    def chemin(self, i, j):
        dists = self.djikstra(i)
        if dists[j][0] == inf:
            return (inf, [])
        else:
            actuel = j
            c = [j]
            while actuel != i:
                c.append(dists[actuel][2])
                actuel = dists[actuel][2]
                print(actuel)
            return (dists[j], c)

def graph_from_ox(G) -> Graph:
    members = [i for i in G.nodes]
    n = G.order()
    adj = np.zeros((n, n))

    orig_adj = [i for i in G.adjacency()]
    for i in range(n):
        successors = [j for j in G.successors(members[i])]
        for j in range(n):
            if members[j] in successors:
                adj[i, j] = orig_adj[i][1][members[j]][0]["length"]

    return Graph(members, adj, ox.plot_graph(G))


def deg(i: int, G: Graph) -> int:
    d = 0
    for j in G.members:
        if G.adj[i, j] != 0:
            d += 1
    return d


# donne le degré infini (évalué a n niveaux de parenté) de chaque point
def deginf(G: Graph, pt: int, lev: int) -> int:
    degG = [deg(i, G) for i in G.members]
    if n == 0:
        return degG[pt]
    deginfG = degG[:]  # liste des deginf des pts de G
    for j in links(G, 0, n):
        deginfG[j] += deginf(G, j, lev - 1)


# donne l'ensemble des noeuds a n niveaux de parenté
def links(G: Graph, pt: int, n: int) -> list:
    if n == 0:
        return None
    L = []
    for i in G.members:
        if G.adj[pt, i] is not None:
            L.append(i)
    for i in L:
        L += links(G, i, n - 1)
    return L


def etendue_minimale_moyenne(G: list):
    M = []
    for i in G.members:
        dists = []
        for j in links(G, i, 1):
            dists.append(G.adj[i, j])
        M.append(min(dists))
    return avg(M)


def avg(L):
    S = 0
    for i in L:
        S += i
    return S / len(L)


def Q1(lst):
    sort = sorted(lst)
    med, i = median(sort)
    return median(sort[:i])


def Q3(lst):
    sort = sorted(lst)
    med, i = median(sort)
    return median(sort[i:])


# supposes une liste triée
def median(lst):
    return lst[len(lst) // 2]


K = Graph(H)
