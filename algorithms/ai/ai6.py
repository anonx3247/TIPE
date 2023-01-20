import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from utils import Utils as ut

MAX_ORDER = 50
NUM_ITERATIONS = 100

class Agent:
    def __init__(self, max_order):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(units=64, activation='relu', input_shape=(max_order, max_order)),
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dense(units=1, activation='relu')
        ])
        self.max_order = max_order

    def _loss(self, env, action, output):
        reward = env.reward(action.numpy())
        expected_reward = ut.expected_reward(env.graph)

        #pi = self.model.weights
        return - tf.math.log(output + 0.0000001)*reward
        #return - tf.math.log(pi)*reward
        

    def action(self, env):
        output = self.model(env.graph, training=True)
        action = tf.reshape(output, (self.max_order,))
        print("Action:", action.numpy())
        loss = self._loss(env, action, output)
        return action.numpy(), loss

    def random_action(self, env):
        output = np.random.rand(env.order)
        action = np.zeros(env.max_order)
        for i in range(env.order):
            action[i] = output[i]
        print("Action:", action)
        action = tf.convert_to_tensor(action, dtype=tf.float32)
        loss = self._loss(env, action, action)
        return action.numpy(), loss



class Environment:
    def __init__(self, max_order):
        self.max_order = max_order
        self.order = 0
        self.graph = np.zeros((max_order, max_order))

    def update(self):
        self.graph, self.order = ut.gen_graph(self.max_order)

    def reward(self, action):
        #path = ut.get_perm(action, np.arange(0, self.max_order, 1))
        path = ut.path_from_list(action, self.order)
        print("Path:", path)
        reward = ut.reward(path, self.graph)

        return reward
        


env = Environment(MAX_ORDER)
env.update()
agent = Agent(MAX_ORDER)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
e = 0.1

batches = 0
avg_reward = []

def train(env, agent, num_iterations, avg_reward, batches, e):
  
    rewards = []
    with tf.GradientTape(persistent=True) as tape:
        for i in range(num_iterations):
            print("Iteration:", i)
            #env.update()

            order = env.order

            #print("Order:", order)
            if np.random.rand(1) < e:
                action, loss = agent.random_action(env)
            else:
                action, loss = agent.action(env)
                #print("Loss:", loss)
                optimizer.minimize(loss, agent.model.variables, tape=tape)
            path = ut.path_from_list(action, env.order)
            reward = ut.reward(path, env.graph)
            print("Reward:", reward)
            rewards.append(reward)
    avg_reward.append(np.mean(rewards))
    batches += 1



