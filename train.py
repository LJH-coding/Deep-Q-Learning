import gymnasium as gym
import numpy as np
import random
from tqdm import tqdm
import torch
from torch.utils.tensorboard import SummaryWriter
from environment import FlappyBirdEnv

env = FlappyBirdEnv()

print("action space = ", env.action_space)
print("observation space = ", env.observation_space)

q_table = np.zeros((env.observation_space.n, env.action_space.n))
writer = SummaryWriter()

# 初始化參數
epsilon = 1
epsilon_decay = 0.9999
epsilon_min = 0.01
gamma = 0.99 # discount factor
lr = 0.1 # learning rate
episodes = 5000000

def epsilon_greedy(state):
    if random.random() < epsilon:
        return env.action_space.sample()
    else:
        return np.argmax(q_table[state])

def update_q(state, action, reward, next_state):
    q_table[state][action] += lr * (reward + gamma * max(q_table[next_state]) - q_table[state][action])

for i in tqdm(range(episodes)):
    state, info = env.reset()
    total_reward = 0
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    
    while True:
        action = epsilon_greedy(state)
        next_state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        if terminated or truncated:
            break
        update_q(state, action, reward, next_state)
        state = next_state
    
    writer.add_scalar("Reward", total_reward, i)
    writer.add_scalar("Epsilon", epsilon, i)

torch_tensor = torch.from_numpy(q_table)
torch.save(torch_tensor, "q_learning.pth")

