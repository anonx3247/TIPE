# What model AI to use?

## Problems

The issue with AI is having training data,
from what I have seen, AI is not actually used to pathfind at all,
that is pretty useless as algorithms like djikstra and A* work perfectly well and arent' as heuristic

The possible solutions then are as follows:

- using AI to select the visiting order of nodes
- using AI to dispatch multiple vehicles to different nodes

### Option 1

For the first we can assume a single driver, and give it a given list of nodes to visit, as well as
graph data like the adjacency matrix, and node degrees, and let it make the choice of which order to visit.

To train it, we can easily make a loss function with the distance travelled, the idea is to calculate the minimum distance
to each and every point prior to the AI working, then to generate an extracted graph with these distances as weights
and the required nodes as nodes, and to run the AI on this graph alone.

If this works then we needn't actually do this step for training: we can simply generate simple graphs arbitrarily large
and then apply the AI once trained on such data.

To train it, we need either a "right answer" i.e. an actual solution to the voyager problem, which can or cannot be optimal,
Otherwise we can create a model like those used in games, which from random noise, generates itself and simply uses
the overall distance as a loss function.

### Option 2

This can be built on top of option 1, the idea here is given *n* nodes  at *l* locations and *p* vehicles,
separate the *n* nodes into *p* groups so as to simplify the voyager problem for each vehicle, and to lower the overall
distance travelled by each one.


The selected method for AI is the MAB or Multi-Armed Bandits model

the state here is identical to the observation and is independent of A: agent actions, and B: previous state.

At any given moment the observation will be defined by an adjacency matrix
with the distances in any given direction from i to j

The action will be an ordered array of the integers, representing the order to visit them in

Once the model is trained on these graphs, we must determine how to generate the extracted graphs:

1. one option is to directly calculate distances for each tuple of points and generate the graph,
this will need to be checked however as running A* n^2 times might be very slow in practice

2. the other option is to define the graph heuristically, either directly through euclidean distance, or with
more granularity, and then to choose the order, finally we only have to run A* on the selected paths given by the AI

Note: we should probably use time as weights however: i.e. distance * average speed.