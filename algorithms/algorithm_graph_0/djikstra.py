# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from heapq import *
from math import inf


# djikstra

G = [
     [0, 1, 0, 4, 2, 0, 0, 0, 0, 0],
     [1, 0, 1, 0, 2, 0, 0, 0, 0, 0],
     [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
     [4, 0, 1, 0, 0, 0, 1, 0, 0, 0],
     [2, 2, 0, 0, 0, 5, 0, 0, 0, 0],
     [0, 0, 0, 0, 5, 0, 2, 0, 0, 0],
     [0, 0, 0, 1, 0, 2, 0, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 1, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 2, 0, 0]
     ]#graphe

def djikstra(sommet, graphe):
    distances = [(inf, i, sommet) for i in range(len(graphe))]
    distances[0] = (0, 0, 0)
    heap = []
    for i in range(len(graphe)):
        heappush(heap, distances[i])
    non_vus = [True for i in graphe]
    sommet_actuel = sommet
    dist_actuelle = 0
    while True in non_vus:
        dist_actuelle, sommet_actuel, origine = heappop(heap)
        distances[sommet_actuel] = (dist_actuelle, sommet_actuel, origine)
        voisins = voisins_a_traiter(sommet_actuel, graphe, non_vus)
        for voisin in voisins:
            heappush(heap, (dist_actuelle + graphe[sommet_actuel][voisin], voisin, sommet_actuel))
        non_vus[sommet_actuel] = False
        
    return distances
    

def voisins_a_traiter(sommet, graphe, non_vus):
    v = []
    for i in range(len(graphe)):
        if graphe[sommet][i] != 0 and non_vus[i]:
            v.append(i)
    return v