import abc
from utils import Utils as u
from matplotlib import pyplot as plt
import numpy as np

import tensorflow as tf
from tf_agents.bandits.environments import bandit_tf_environment
from tf_agents.policies import actor_policy, tf_policy
from tf_agents.specs import tensor_spec
from tf_agents.trajectories import trajectory, policy_step, time_step as ts
from tf_agents.drivers import dynamic_step_driver
from tf_agents.agents import tf_agent
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.metrics import tf_metrics

MAX_ORDER = 30
BATCH_SIZE = 8
NUM_ITERATIONS = 100
STEPS_PER_LOOP = 2

class GraphEnvironment(bandit_tf_environment.BanditTFEnvironment):
    def __init__(self, max_order):
        self.max_order = max_order
        action_spec = tensor_spec.BoundedTensorSpec(
            shape = (),
            dtype = tf.float64,
            minimum = 0,
            maximum = 1,
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

        super(GraphEnvironment, self).__init__(
            time_step_spec,
            action_spec
        )

    def _observe(self):
        self._observation = tf.convert_to_tensor(u.gen_graph(self.max_order), dtype=tf.float64)
        return self._observation

    def _apply_action(self, action):
        order = u.get_order(self._observation)
        perm = u.get_perm(action, [i for i in range(order)])
        return u.reward(perm, self._observation.numpy())


class GraphNet(network.Network):
    def __init__(self, observation_spec, action_spec):
        super(GraphNet, self).__init__(
            input_tensor_spec = observation_spec,
            state_spec = (),
            name = "GraphNet"
        )

        self._action_spec = action_spec
        self._action_projection_layer = tf.keras.layers.Dense(
            action_spec.shape.num_elements(),
            activation=tf.nn.tanh
        )

    def call(self, observations, step_type = (), network_state = ()):
        outer_rank = nest_utils.get_outer_rank(observations, self.input_tensor_spec)
        


env = GraphEnvironment(MAX_ORDER)
