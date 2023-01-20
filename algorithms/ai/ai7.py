from matplotlib import pyplot as plt
import numpy as np
from utils import Utils as ut
import tensorflow as tf

from tf_agents.agents import tf_agent.
from tf_agents.policies import tf_policy
from tf_agents.environments import TFEnvironment
from tf_agents.specs import tensor_spec


class GraphEnvironment(bandit_tf_environment.BanditTFEnvironment):
    def __init__(self, max_order):
        self.max_order = max_order
        action_spec = tensor_spec.BoundedTensorSpec(
            shape = (max_order,),
            dtype = tf.uint8,
            minimum = 0,
            maximum = max_order-1,
            name = 'selection'
        )

        observation_spec = tensor_spec.BoundedTensorSpec(
            shape = (max_order, max_order),
            dtype = tf.float32,
            minimum = 0,
            maximum = 1,
MAX_ORDER = 50


# environment is defined as the adjacency matrix of a graph
class GraphEnvironment(bandit_tf_environment.BanditTFEnvironment):
    def __init__(self, max_order):
        self.max_order = max_order
        action_spec = tensor_spec.BoundedTensorSpec(
            shape = (max_order,),
            dtype = tf.uint8,
            minimum = 0,
            maximum = max_order-1,
            name = 'selection'
        )
            name = 'graph'
        )

        time_step_spec = ts.time_step_spec(observation_spec)
        super(GraphEnvironment, self).__init__(time_step_spec, action_spec)

    def initialize(self):
        self._observation = u.gen_graph(self.max_order)

    def _observe(self):
        return self._observation

    def _apply_action(self, action):
        return u.reward(action, self._observation)