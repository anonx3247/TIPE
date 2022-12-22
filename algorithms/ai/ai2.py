#from graph import Graph
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf
from tf_agents.networks import network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.bandits.agents.examples.v2 import trainer
from tf_agents.networks import q_network
from tf_agents.bandits.environments import bandit_tf_environment
from tf_agents.specs import array_spec
from tf_agents.specs import tensor_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.trajectories import trajectory


MAX_ORDER = 50
BATCH_SIZE = 8
CONTEXT_DIM = 15
NUM_ACTIONS = 5
REWARD_NOISE_VARIANCE = 0.01
TRAINING_LOOPS = 400
STEPS_PER_LOOP = 2


def gen_graph(max_order: int) -> np.array:
    assert(max_order >= 3)
    order = np.random.randint(3, max_order+1)
    G = np.random.rand(order, order)
    K = np.zeros((max_order, max_order))
    for i in range(order):
        for j in range(order):
            K[i,j] = G[i,j]
    return K

def get_order(graph):
    order = len(graph)
    # calculate order:
    for i in range(len(graph)):
        if graph[i,i] == 0 and order > i:
            order = i
    return order
    

def reward(path, graph):

    order = get_order(graph)
    max_reward = order**2

    reward = 0

    # check presence of each node and repetitions:
    present = [0 for i in range(order)]
    sum = 0
    for i in range(order):
        if i in path:
            present[i] += 1

    for i in present:
        if i != 0:
            sum += 1

    # reward if all nodes present
    if sum >= order:
        reward += 1
    else:
        reward -= order


    # punish for long distances
    dist = 0
    for i in range(order-1):
        node = int(path[i])
        next_node = int(path[i+1])
        dist += graph[node, next_node]

    reward += max_reward - dist

    return reward / max_reward

    

# utility class to have MBA instead of regular reinforcement learning
class GraphEnvironment(bandit_tf_environment.BanditTFEnvironment):

    def __init__(self, max_order):
        action_spec = tensor_spec.BoundedTensorSpec(
            shape = (max_order,),
            dtype = tf.uint8,
            minimum = 0,
            maximum = max_order-1,
            name = 'selection'
        )

        observation_spec = tensor_spec.BoundedTensorSpec(
            shape = (max_order, max_order),
            dtype = tf.float64,
            minimum = 0,
            maximum = 1,
            name = 'graph'
        )
        time_step_spec = ts.time_step_spec(observation_spec)
        # action_spec = array_spec.BoundedArraySpec(
            # shape = (max_order,),
            # dtype = np.uint8,
            # minimum = 0,
            # maximum = max_order-1,
            # name = 'selection'
        # )
# 
        # observation_spec = array_spec.BoundedArraySpec(
            # shape = (max_order, max_order),
            # dtype = np.float64,
            # minimum = 0,
            # maximum = 1,
            # name = 'graph'
        # )
        super(GraphEnvironment, self).__init__(time_step_spec, action_spec, BATCH_SIZE)

    def _observe(self):
        self._observation = gen_graph(self.max_order)
        return self._observation

    def _apply_action(self, action):
        return reward(action, self._observation)



def expected_reward(observation):
    order = get_order(observation)
    exp_reward = order**2
    exp_reward += 1
    return exp_reward
    

environment = GraphEnvironment(MAX_ORDER)




q_net = q_network.QNetwork(
        environment.observation_spec(),
        environment.action_spec(),
        fc_layer_params=(50, 50))

agent = dqn_agent.DqnAgent(
        environment.time_step_spec(),
        environment.action_spec(),
        q_network=q_net,
        epsilon_greedy=0.1,
        target_update_tau=0.05,
        target_update_period=5,
        optimizer=tf.compat.v1.train.AdamOptimizer(learning_rate=1e-2),
        td_errors_loss_fn=common.element_wise_squared_loss)

regret_metric = tf_bandit_metrics.RegretMetric(expected_reward)

trainer.train(
        root_dir=FLAGS.root_dir,
        agent=agent,
        environment=environment,
        training_loops=TRAINING_LOOPS,
        steps_per_loop=STEPS_PER_LOOP,
        additional_metrics=[regret_metric])
