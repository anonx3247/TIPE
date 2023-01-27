#from graph import Graph
import abc
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf
from tf_agents.networks import network
from tf_agents.agents import tf_agent
from tf_agents.drivers import driver
from tf_agents.bandits.environments import bandit_tf_environment
from tf_agents.policies import tf_policy
from tf_agents.policies import actor_policy
from tf_agents.specs import array_spec
from tf_agents.specs import tensor_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.trajectories import trajectory
from tf_agents.trajectories import policy_step
from utils import Utils as u


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

        observation_spec = tensor_spec.BoundedTensorSpec(
            shape = (max_order, max_order),
            dtype = tf.float32,
            minimum = 0,
            maximum = 1,
            name = 'graph'
        )

        time_step_spec = ts.time_step_spec(observation_spec)
        super(GraphEnvironment, self).__init__(time_step_spec, action_spec)

    def _observe(self):
        self._observation = u.gen_graph(self.max_order)
        return self._observation

    def _apply_action(self, action):
        return u.reward(action, self._observation)


# we use a neural network to select the action to take
class ActionNetwork(network.Network):
    def __init__(self, input_tensor_spec, output_tensor_spec):
        super(ActionNetwork, self).__init__(
            input_tensor_spec=input_tensor_spec,
            state_spec=(),
            name='ActionNetwork')
        self._output_tensor_spec = output_tensor_spec
        self._sub_layers = [
            tf.kera.layers.Dense(
                input_tensor.spec.shape.num_elements(), activation=tf.nn.relu
            ),
            tf.kera.layers.Dense(
                output_tensor_spec.shape.num_elements(), activation=tf.nn.relu
            ),
            tf.keras.layers.Dense(
                output_tensor_spec.shape.num_elements(), activation=tf.nn.tanh
            )
        ]

    def call(self, observations, step_type, network_state):
        del step_type

        output = tf.cast(observations, dtype=tf.float64)
        for layer in self._sub_layers:
          output = layer(output)
        actions = tf.reshape(output, [-1] + self._output_tensor_spec.shape.as_list())

        # Scale and shift actions to the correct range if necessary.
        return actions, network_state

class GraphPolicy(actor_policy.ActorPolicy):
    def __init__(self, observation_spec, action_spec):
        time_step_spec = ts.time_step_spec(observation_spec)
        super(GraphPolicy, self).__init__(
            time_step_spec=time_step_spec,
            action_spec=action_spec,
            actor_network=ActionNetwork(observation_spec, action_spec)
        )
        

class GraphAgent(tf_agent.TFAgent):
    def __init__(self, observation_spec, action_spec):
        policy = GraphPolicy(observation_spec, action_spec)
        time_step_spec = policy.time_step_spec
        super(GraphAgent, self).__init__(
            time_step_spec = time_step_spec,
            action_spec = action_spec,
            policy = policy,
            collect_policy = policy,
            train_sequence_length = None
        )

    def _initialize(self):
        pass
        

    def _train(self, experience, weights=None):
        observation = experience.observation
        action = experience.action
        reward = experience.reward

        

environment = GraphEnvironment(MAX_ORDER)
# tf_environment = tf_py_environment.TFPyEnvironment(environment)
tf_environment = environment

time_step_spec = ts.time_step_spec(observation_spec)

action_net = ActionNetwork(
    tf_environment.observation_spec(),
    tf_environment.action_spec()
)

intelligent_policy = actor_policy.ActorPolicy(
    time_step_spec=time_step_spec,
    action_spec=tf_environment.action_spec,
    actor_network=action_net
)

regret = tf.metrics.RegretMetric(expected_reward)

def train(env, act_net, policy, num_iterations, steps_per_loop, regret_metric):
    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        data_spec = policy.trajectory_spec,
        batch_size = 2,
        max_length = steps_per_loop
    )

    observers = [replay_buffer.add_batch, regret_metric]

    driver = dynamic_step_driver.DynamicStepDriver(
        env = env,
        policy = policy,
        num_steps = steps_per_loop * batch_size,
        observers = observers
    )

    regret_values = []

    for _ in range(num_iterations):
        driver.run()
        loss_info = agent.train(replay_buffer.gather_all())
        replay_buffer.clear()
        regret_values.append(regret_metric.result())

    plt.plot(regret_values)
    plt.ylabel('Average Regret')
    plt.xlabel('Number of Iterations')

