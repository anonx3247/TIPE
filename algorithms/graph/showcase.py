from matplotlib import pyplot as plt
from graph import Graphe
import osmnx as ox
import numpy as np

adresse = "1 Venelle Artémis, Sait Germain en Laye, France"

print("Voici un graphe de l'adresse", adresse)

G = Graphe(adresse=adresse, nom='artemis')

print("Démonstration de recherche Djikstra...")

G.djikstra(0, animate=True)

print("Voici le noeud 5:")

G.plot_noeud(5)

plt.show()

print("Chemin de 3 a 443 avec A*:")

G.A_star(3, 443, animate=True)

print("Chemin de 12 a 443")

G.chemin(12, 443, show=True)

plt.show()

print("La distance du plus court chemin de 7 a 85 est de", int(G.dist(7, 85)), "mètres")