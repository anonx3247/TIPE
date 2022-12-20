from matplotlib import pyplot as plt
from graph import Graph
import osmnx as ox
import numpy as np

G = Graph(address="1 Venelle Artémis, Saint Germain en Laye, France", name='artemis')

print("Showing Djikstra search...")

G.djikstra(0, animate=True)

print("Showing Node 5")

G.plot_node(5)

plt.show()

print("Showing Path from node 0 to node 443")

G.chemin(0, 443, show=True)

plt.show()

print("The distance on the shortest path from 7 to 85 is: ", int(G.dist(7, 85)), "meters")