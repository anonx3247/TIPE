import abc
from utils import Utils as u
from matplotlib import pyplot as plt
import numpy as np

import tensorflow as tf
from tf_agents.bandits.environments import bandit_py_environment, bandit_tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.policies import actor_policy, tf_policy
from tf_agents.specs import tensor_spec, array_spec
from tf_agents.trajectories import trajectory, policy_step, time_step as ts
from tf_agents.drivers import dynamic_step_driver
from tf_agents.agents import tf_agent
from tf_agents.train import Actor
from tf_agents.networks import network
from tf_agents.bandits.agents import greedy_multi_objective_neural_agent
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
            shape = (max_order,),
            dtype = tf.uint8,
            minimum = 0,
            maximum = max_order,
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
        return u.reward(action, self._observation.numpy())

class GraphNet(network.Network):
    def __init__(self, input_tensor_spec, output_tensor_spec):
        super(GraphNet, self).__init__(
            input_tensor_spec = input_tensor_spec,
            state_spec = (),
            name = "GraphNet"
        )

        self._output_tensor_spec = output_tensor_spec
        self._sub_layers = [
            tf.keras.layers.Dense(
                input_tensor_spec.shape.num_elements(), activation = tf.nn.tanh
            ),
            tf.keras.layers.Dense(
                output_tensor_spec.shape.num_elements(), activation = tf.nn.tanh
            ),
            tf.keras.layers.Dense(
                output_tensor_spec.shape.num_elements(), activation = tf.nn.relu
            )
        ]

    def call(self, observations, step_type, network_state):
        del step_type

        output = tf.cast(observations, dtype=tf.float64)
        for layer in self._sub_layers:
            output = layer(output)
        output = tf.cast(output, tf.uint8)
        actions = tf.reshape(output, [-1] + self._output_tensor_spec.shape.as_list(),)
        #actions = output
        return actions, network_state

#class GraphAgent(tf_agent.TFAgent):
    #def __init__(self, time_step_spec, action_spec, policy):
        #super(GraphAgent, self).__init__(
            #time_step_spec = time_step_spec,
            #action_spec = action_spec,
            #policy = policy
        #)
#
    #def _train(self, experience, weights=None):
        #observation = experience.observation
        #action = experience.action
        #reward = experience.reward
#
        #return tf_agent.LossInfo()

def trajectory_gen(initial_step, action_step, final_step):
    return trajectory.Trajectory(
        observation = tf.expand_dims(initial_step.observation, 0),
        action = tf.expand_dims(action_step.action, 0),
        policy_info = action_step.info,
        reward = tf.expand_dims(final_step.reward, 0),
        discount = tf.expand_dims(final_step.discount, 0),
        step_type = tf.expand_dims(initial_step.step_stype, 0),
        next_step_type = tf.expand_dims(final_step.step_type, 0)
    )

env = GraphEnvironment(MAX_ORDER)
net = GraphNet(env.observation_spec(), env.action_spec())
policy = actor_policy.ActorPolicy(
    time_step_spec = env.time_step_spec(),
    action_spec = env.action_spec(),
    actor_network = net
)

#agent = GraphAgent(
    #time_step_spec=env.time_step_spec(),
    #action_spec=env.action_spec(),
    #policy=policy,
    #collect_policy=policy
#)

agent = greedy_multi_objective_neural_agent.GreedyMultiObjectiveNeuralAgent(
    time_step_spec = env.time_step_spec(),
    action_spec = env.action_spec(),
    scalarizer = ...,
    objective_network_and_loss_fn_sequence = [(net, loss)]
)

replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec = agent.policy_trajectory_spec,
    batch_size = BATCH_SIZE,
    max_length = STEPS_PER_LOOP
)

regret_metric = tf_metrics.RegretMetric(lambda x : u.expected_reward(x.numpy()))

observers = [replay_buffer.add_batch, regret_metric]

driver = dynamic_step_driver.DynamicStepDriver(
    env = env,
    policy = policy,
    observers = observers,
    num_steps = STEPS_PER_LOOP * BATCH_SIZE
)


# Training

def train1(env, agent, num_iterations):
    step = env.reset()
    for _ in range(num_iteration):
        action_step = agent.collect_policy.action(step)
        next_step = env.step(action_step.action)
        experience = trajectory_gen(step, action_step, next_step)
        print(experience)
        agent.train(experience)
        step = next_step
def train2(driver, replay_buffer, num_iterations):
    regret_values = []
    for _ in range(num_iterations):
        driver.run()
        loss_info = agent.train(replay_buffer.gather_all())
        replay_buffer.clear()
        regret_values.append(regret_metric.result())

    plt.plot(regret_values)
    plt.ylabel("Average Regret")
    plt.xlabel("Number of Iterations")
    plt.show()
        

    
def train3(env, policy, num_iterations):
    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        data_spec = agent.policy_trajectory_spec,
        batch_size = BATCH_SIZE,
        max_length = STEPS_PER_LOOP
    )

    regret_metric = tf_metrics.RegretMetric(lambda x : u.expected_reward(x.numpy()))

    observers = [replay_buffer.add_batch]
    metrics = [regret_metric]

    init_step = env.reset()

    actor = Actor(
        env, 
        policy, 
        init_step, 
        steps_per_run=2, 
        episodes_per_run=1, 
        observers=observers,
        metrics=metrics
    )

    for _ in range(num_iterations):
        actor.run()



        
                
        
    