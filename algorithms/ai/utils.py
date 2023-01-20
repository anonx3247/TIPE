#from graph import Graph
from matplotlib import pyplot as plt
import numpy as np


class Utils:
    #def gen_graph(max_order: int) -> np.array:
        #assert(max_order >= 3)
        #order = np.random.randint(3, max_order+1)
        #G = np.random.rand(order, order)
        #K = np.zeros((max_order, max_order))
        #for i in range(order):
            #for j in range(order):
                #K[i,j] = G[i,j]
        #return K, order

    def gen_graph(max_order: int) -> np.array:
            assert(max_order >= 3)
            G = np.random.rand(max_order, max_order)
            return G, max_order

    def get_order(graph):
        order = len(graph)
        # calculate order:
        for i in range(len(graph)):
            if graph[i,i] == 0 and order > i:
                order = i
        return order

    def all_present(order, path):
        for i in range(order):
            if not i in path:
                return False
        if len(path) != order:
            return False
        else:
            return True

        return validated
    
    def reward(path, graph):
        order = len(path)
        dist = 0
        for i in range(order-1):
            node = int(path[i])
            next = int(path[i+1])
            dist += graph[node, next]

        return 1-dist/order**2

    #def reward(path, graph):
#
        #order = Utils.get_order(graph)
        #max_reward = order**2
#
        #reward = 0
#
        ## check presence of each node and repetitions:
        #present = [0 for i in range(order)]
        #sum = 0
        #for i in range(order):
            #if i in path:
                #present[i] += 1
#
        #for i in present:
            #if i != 0:
                #sum += 1
#
        ## reward if all nodes present
        #if sum >= order:
            #reward += 1
        #else:
            #reward -= order
#
#
        ## punish for long distances
        #dist = 0
        #for i in range(order-1):
            #node = int(path[i])
            #next_node = int(path[i+1])
            #dist += graph[node, next_node]
#
        #reward += max_reward - dist
#
        #return reward / max_reward

    

    def expected_reward(observation):
        order = Utils.get_order(observation)
        exp_reward = order**2
        exp_reward += 1
        return exp_reward

    def get_perm(code: float, L: list) -> [int]:
        rep = str(code*10**len(L))[:-2] # remove the .0 from the float
        rep = [int(i) for i in rep]
        print(rep)
        F = []

        for i in rep:
            F.append(L.pop(i))

        return np.array(F)

    def path_from_list(A: np.array, order: int) -> [int]:
        L = [i for i in A]
        sort = sorted(L[:order])
        mapping = {}
        for i in range(order):
            mapping[sort[i]] = i

        return np.array([mapping[j] for j in L[:order]])
            

    
