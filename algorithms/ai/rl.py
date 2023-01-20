from matplotlib import pyplot as plt
import numpy as np
from utils import Utils as ut

import tensorflow as tf
from tf_agents.environments import py_environment, utils, tf_py_environment
from tf_agents.agents.reinforce import reinforce_agent
from tf_agents.drivers import py_driver
from tf_agents.networks import actor_distribution_network
from tf_agents.specs import tensor_spec, array_spec
from tf_agents.trajectories import trajectory, time_step as ts


# Define Environment

class GraphEnvironment(py_environment.PyEnvironment):
    def __init__(self, max_order):
        self._action_spec = array_spec.BoundedArraySpec(
            shape = (),
            dtype = np.uint64,
            minimum = 0,
            maximum = max_order-1
        )

        self._observation_spec = array_spec.BoundedArraySpec(
            shape = (max_order, max_order),
            dtype = np.float64,
            minimum = 0,
            maximum = 1
        )

        self.max_order = max_order
        graph, order = ut.gen_graph(self.max_order)
        self.order = order
        # state is (graph, path, current_distance)
        self._state = [graph, [], 0]
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        graph, order = ut.gen_graph(self.max_order)
        self._state = [graph, [], 0]
        self._episode_ended = False
        return ts.restart(self._state[0])

    def _step(self, action):

        if self._episode_ended:
            return self.reset()
        elif len(self._state[1]) == self.order:
            self._episode_ended = True
        else:
            # add selected node to path
            self._state[1].append(action)
            # add distance
            self._state[2] += self._state[0][self._state[1][-2], self._state[1][-1]] if len(self._state[1]) >= 2 else 0

        if self._episode_ended or len(self._state[1]) >= self.order:
            reward = self.order**2 - self._state[2] if ut.all_present(self.order, self._state[1]) else -self.order**2
            return ts.termination(self._state[0], reward)
        else:
            return ts.transition(self._state[0], reward = 0.0, discount = 1.0)


env = GraphEnvironment(50)

# validate environment
utils.validate_py_environment(env, 5)

# test actions
initial_time_step = env.reset()
print(initial_time_step)
print(env._state)
action = np.uint64(1)
next_time_step = env.step(action)
print(next_time_step)
print(env._state)

# convert py to tf env

tf_env = tf_py_environment.TFPyEnvironment(env)

print(tf_env.action_spec())
print(tf_env.observation_spec())

# create actor network

actor_net = actor_distribution_network.ActorDistributionNetwork(
    tf_env.obseobservation_spec(),
    tf_env.actioaction_spec(),
    dtype=tf.float64
)

optimizer = tf.keras.optimizers.Adam()

train_step_counter = tf.Variable(0)

tf_agent = reinforce_agent.ReinforceAgent(
    time_step_spec = tf_env.time_step_spec(),
    action_spec = tf_env.action_spec(),
    actor_network = actor_net,
    optimizer = optimizer,
    normalize_returns = True,
    train__step_counter = train_step_counter
)

tf_agent.initiaalize()

eval_policy = tf_agent.policy
collect_policy = tf_agent.colllect_policy

def compute_avg_ret(env, policy, num_episodes=10):
    total = 0
    for _ in range(num_episodes):
        time_step = env.reset()
        ep_ret = 0
        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = env.step(action_step.action)
            ep_ret += time_step.reward

        tot_ret += ep_ret

        avg_ret = tot_ret / num_episodes
        return avg_ret.numpy()[0]
            


        
        