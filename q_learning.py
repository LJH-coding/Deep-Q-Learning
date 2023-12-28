import numpy as np
import random
from environment import Environment
import pickle

class QAgent():
    def __init__(self):
        # define initial parameters
        self.discount_rate = 0.9 #gamma
        self.learning_rate = 0.0001
        self.eps = 1.0
        self.eps_discount = 0.9999992
        self.min_eps = 0.01
        self.num_episodes = 50000000
        self.table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2))
        self.env = Environment()
        self.reward = []
        
    # epsilon-greedy action choice
    def get_action(self, state):
        # select random action (exploration)
        if random.random() < self.eps:
            return random.choice([0, 1])
        
        # select best action (exploitation)
        return np.argmax(self.table[state])
    
    def train(self):
        for i in range(1, self.num_episodes + 1):
            self.env.reset()
            
            # print updates
            if i % 10000 == 0:
                print(f"Episodes: {i}, reward: {np.mean(self.reward)}, eps: {self.eps}, lr: {self.learning_rate}")
                self.reward = []
               
            # occasionally save latest model
            if (i % 500000 == 0):
                with open(f'pickle/{i}.pickle', 'wb') as file:
                    pickle.dump(self.table, file)
                
            current_state = self.env.get_state()
            self.eps = max(self.eps * self.eps_discount, self.min_eps)
            done = False
            total_reward = 0
            while not done:
                # choose action and take it
                action = self.get_action(current_state)
                new_state, reward, done = self.env.step(action)
                total_reward += reward
                
                # Bellman Equation Update
                self.table[current_state][action] = (1 - self.learning_rate)\
                    * self.table[current_state][action] + self.learning_rate\
                    * (reward + self.discount_rate * max(self.table[new_state])) 
                current_state = new_state

                #self.env.render()
            
            # keep track of important metrics
            self.reward.append(total_reward)

def random_agent():
    if random.random() < 0.5:
        return 1
    else:
        return 0
    
AI = QAgent()
AI.train()
