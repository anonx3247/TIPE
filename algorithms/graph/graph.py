# pour operations de graphe
import numpy as np
import osmnx as ox
from matplotlib import pyplot as plt

# pour l'animation
from matplotlib.animation import FuncAnimation as fn_anim

# pour djikstra et A* algorithm
from heapq import *
from math import inf, sqrt

# pour les operations de fichier
from os.path import exists

class Graphe:
    """
    Un Graphe est un objet enregistrant a la fois le graphe osmnx
    ainsi qu'une forme plus exploitable, notamment avec des neouds indices de 0
    a n et muni d'une matrice d'adjacence, et de nombreuses methodes pour faciliter
    son exploitation
    """
    def __init__(self, G=None, emplacement=None, adresse=None, nom=None):
        assert(G != None or adresse != None or emplacement != None or nom != None)
        if nom != None and exists(nom + ".gml"):
            G = ox.load_graphml(nom+".gml")
        else:
            if G == None and adresse != None and emplacement == None:
                G = ox.graph_from_adresse(adresse)
                ox.save_graphml(G, nom+".gml")
            elif G == None and adresse == None and emplacement != None:
                G = ox.graph_from_emplacement(emplacement)
                ox.save_graphml(G, nom+".gml")
            elif G == None and adresse == None and emplacement == None:
                G = ox.load_graphml(nom+".gml")
        
        membres = [i for i in G.nodes]
        n = G.order()
        adj = {}

        orig_adj = [i for i in G.adjacency()]
        for i in range(n):
            successeurs = [j for j in G.successors(membres[i])]
            for j in range(n):
                if membres[j] in successeurs:
                    adj[i, j] = orig_adj[i][1][membres[j]][0]["length"]

        self.nom = nom
        self.membres = membres
        self.adj = adj
        self.rep = ox.plot_graph(G, save=True, filepath=nom+".png")
        self.ordre = len(membres)
        self.graphe = G
        self.dists_from = {}
        self.chemins = {}

    def deg(self, i: int) -> int:
        """
        renvoie le degre d'un point
        """
        d = 0
        for j in range(self.ordre):
            if (i,j) in self.adj:
                d += 1
        return d

    def liaisons(self, pt: int, n: int) -> list:
        """
        renvoie les noeuds a n degres de parente de pt
        """
        if n == 0:
            return []
        S = []
        L = []
        for i in range(self.ordre):
            if (pt, i) in self.adj:
                L.append(i)
        S += L
        for i in L:
            S += self.liaisons(i, n - 1)
        return S

    def deginf(self, pt: int, lev: int) -> int:
        """
        donne le degré infini (évalué a n niveaux de parenté) de chaque point
        """
        degG = self.deg(pt)
        if lev == 0:
            return degG
        deginfG = degG  # liste des deginf des pts de G
        for j in self.liaisons(pt, lev):
            deginfG += self.deginf(j, lev - 1)
        return deginfG

    def plot_noeud(self, i: int):
        """
        affiche le noeud sur l'image du graphe
        """
        bkg = ox.plot_graph(self.graphe, show=False)
        x, y = self.coordonnes(pt=i)
        plt.scatter([x], [y], color='blue')

    def plot_noeuds(self, L: list):
        """
        affiche les noeuds sur l'image du graphe
        """
        coords = self.coordonnes(pts=L)
        x = [i[0] for i in coords]
        y = [i[1] for i in coords]
        bkg = ox.plot_graph(self.graphe, show=False)
        plt.plot(x, y, color = 'green')

    def plot_chemin(self, chemin: list):
        """
        affiche les noeuds sur l'image du graphe
        """
        coords = self.coordonnes(pts=chemin)
        x = [i[0] for i in coords]
        y = [i[1] for i in coords]
        bkg = ox.plot_graph(self.graphe, show=False)
        plt.plot(x, y,
                color = 'red',
                linestyle = 'solid',
                marker = 'o')

    def plot_voisins(self, i: int, n: int):
        """
        montre les voisins sur l'image, a n degres de parente
        """
        L = self.liaisons(i, n)
        self.plot_noeuds(L)

    def plot(self):
        ox.plot_graph(self.graphe)

    def coordonnes(self, pt: int = None, pts: list = None) -> tuple:
        assert(pt != None or pts != None)
        if pt == None:
            return [self.coordonnes(pt=i) for i in pts]
        else:
            id = self.membres[pt]
            x = self.graphe.nodes[id]['x']
            y = self.graphe.nodes[id]['y']
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
        distances = [(inf, i, None) for i in range(self.ordre)]
        distances[sommet] = (0, sommet, sommet)
        heap = []
        for i in range(self.ordre):
            heappush(heap, distances[i])
        non_vus = [True for i in self.adj]
        sommet_actuel = sommet
        dist_actuelle = 0

        while True in non_vus:
            dist_actuelle, sommet_actuel, origine = heappop(heap)
            if animate:
                xi, yi = self.coordonnes(sommet_actuel)
                vus.append([self.coordonnes(i) for i in range(len(non_vus)) if not non_vus[i]])
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
        ancetres = [k for (i, j, k) in distances]
        ancetres[sommet] = None
        for i in range(self.ordre):
            self.chemins[sommet, i] = self.reconstitue_chemin(ancetres, i)
        
        if animate:
            fig, ax = plt.subplots()

            vus_x = [ [x for (x,y) in i] for i in vus]
            vus_y = [ [y for (x,y) in i] for i in vus]

            bkg = ox.plot_graph(self.graphe, ax=ax, show=False)

            step = self.ordre//100

            animation = fn_anim(fig,
                        func = self.djikstra_anim,
                        fargs = (x, y, ax, vus_x, vus_y, step),
                        frames = np.arange(0, len(x)//step, 1),
                        interval = 0.0001,
                        repeat = False)
            if save:
                animation.save('djikstra_' + self.nom + '_' + str(sommet) + '.mp4', 
                                writer='ffmpeg',
                                dpi=300)
            else:
                plt.show()
        return distances

    def dist_euclidienne(self, i: int, j: int):
        x1, y1 = self.coordonnes(i)
        x2, y2 = self.coordonnes(j)
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
        distances = [(inf, i, None) for i in range(self.ordre)]
        distances[debut] = (self.dist_euclidienne(debut, fin), 0, debut)
        heap = []
        for i in range(self.ordre):
            heappush(heap, distances[i])
        non_vus = [True for i in self.adj]
        sommet_actuel = debut
        dist_possible = self.dist_euclidienne(debut, fin)
        dist_actuelle = 0
        ancetres = [i for i in range(self.ordre)]
        ancetres[debut] = None

        while True in non_vus:
            dist_possible, dist_actuelle, sommet_actuel = heappop(heap)
            origine = ancetres[sommet_actuel]
            if animate:
                xi, yi = self.coordonnes(sommet_actuel)
                vus.append([self.coordonnes(i) for i in range(len(non_vus)) if not non_vus[i]])
                x.append(xi)
                y.append(yi)
            if sommet_actuel == fin:
                break
            distances[sommet_actuel] = (dist_possible, dist_actuelle, sommet_actuel)
            voisins = self.voisins_a_traiter(sommet_actuel, non_vus)
            for voisin in voisins:
                heappush(heap, (dist_actuelle + self.adj[sommet_actuel,voisin] + self.dist_euclidienne(sommet_actuel, fin), 
                                dist_actuelle,
                                voisin))
                ancetres[voisin] = sommet_actuel
            non_vus[sommet_actuel] = False

        chemin = self.reconstitue_chemin(ancetres, fin)
        
        if animate:
            print("chemin trouvé, animation en cours...")
            fig, ax = plt.subplots()

            vus_x = [ [x for (x,y) in i] for i in vus]
            vus_y = [ [y for (x,y) in i] for i in vus]

            bkg = ox.plot_graph(self.graphe, ax=ax, show=False)

            step = self.ordre//100

            animation = fn_anim(fig,
                        func = self.A_anim,
                        fargs = (x, y, ax, vus_x, vus_y, step, chemin),
                        frames = np.arange(0, len(x)//step + step, 1),
                        interval = 200,
                        repeat = False)
            if save:
                animation.save('A_star_' + self.nom + '_' + str(debut) + '_' + str(fin) + '.mp4', 
                                writer='ffmpeg',
                                dpi=300)
            else:
                plt.show()
        
        self.chemins[(debut, fin)] = chemin
        return chemin

    def reconstitue_chemin(self, ancetres, fin):
        i = fin
        chemin = [i]
        while ancetres[i] != None:
            chemin.append(ancetres[i])
            i = ancetres[i]
        chemin.reverse()
        return chemin

    def djikstra_anim(self, i, x, y, ax, vus_x, vus_y, step):
        ax.scatter(vus_x[i*step], vus_y[i*step], color='blue')
        ax.scatter(x[max(0, i*step-step):i*step], y[max(0, i*step-step):i*step], color="red")

    def A_anim(self, i, x, y, ax, vus_x, vus_y, step, chemin):
        if i <= len(x)//step:
            ax.scatter(vus_x[i*step], vus_y[i*step], color='blue')
            ax.scatter(x[max(0, i*step-step):i*step], y[max(0, i*step-step):i*step], color="red")
        else:
            x = [self.coordonnes(i)[0] for i in chemin]
            y = [self.coordonnes(i)[1] for i in chemin]
            ax.plot(x, y, color='red')
        

    def voisins_a_traiter(self, sommet: int, non_vus: list) -> list:
        v = []
        for i in range(self.ordre):
            if (sommet,i) in self.adj and non_vus[i] and i != sommet:
                v.append(i)
        return v

    def dist(self, i: int, j: int) -> float:
        """
        returns distance between i and j 
        """
        c = self.chemin(i,j)
        d = 0
        for i in range(len(c) - 1):
            d += self.adj[c[i], c[i+1]]
        return d
            
            

    def chemin(self, i: int, j: int, show=False) -> (float, list):
        """
        renvoie le chemin le plus court de i a j
        et la distance de ce parcours
        """
        c = self.A_star(i,j)
        if show:
            self.plot_chemin(c)
            plt.show()
        return c
