import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from utils import Utils as ut

MAX_ORDER = 50
NUM_ITERATIONS = 10000

class Agent:
    def __init__(self, e, max_order, learning_rate):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(units=64, activation='relu', input_shape=(max_order, max_order)),
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dense(units=1, activation='relu')
        ])
        self.max_order = max_order
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, epsilon=e)

    def _loss(self, env, action):
        reward = env.reward(action.numpy())
        expected_reward = ut.expected_reward(env.graph)

        advantage = expected_reward - reward

        pi = self.model.weights
        return - tf.math.log(action + 0.0001)*advantage
        #return tf.math.log(pi)*advantage
        

    def action(self, env, tape):
        output = self.model(env.graph, training=True)
        action = tf.reshape(output, (self.max_order,))
        print("Action:", action.numpy())
        loss = self._loss(env, action)
        self.optimizer.minimize(loss, self.model.variables, tape=tape)
        return action.numpy(), loss

    def random_action(self, env, tape):
        output = np.random.rand(env.order)
        action = np.zeros(env.max_order)
        for i in range(env.order):
            action[i] = output[i]
        print("Action:", action)
        action = tf.convert_to_tensor(action, dtype=tf.float32)
        loss = self._loss(env, action)
        self.optimizer.minimize(loss, self.model.variables, tape=tape)
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
agent = Agent(0.1, MAX_ORDER, 0.001)

def train(env, agent):
    with tf.GradientTape(persistent=True) as tape:
        for i in range(NUM_ITERATIONS):
            print("Iteration:", i)
            env.update()

            order = env.order

            print("Order:", order)
            if i % 50 == 0:
                action, loss = agent.random_action(env, tape)
            else:
                action, loss = agent.action(env, tape)
            path = ut.path_from_list(action, env.order)
            print("Reward:", ut.reward(path, env.graph))
            print("Loss:", loss)