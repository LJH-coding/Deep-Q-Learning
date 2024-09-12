import gymnasium as gym
import numpy as np
from tqdm import tqdm
import torch
from environment import FlappyBirdEnv

def evaluate_agent(env, n_eval_episodes, Q):
    episode_rewards = []
    for episode in tqdm(range(n_eval_episodes)):
        state, info = env.reset()
        step = 0
        truncated = False
        terminated = False
        total_rewards_ep = 0

        while True:
            # Take the action (index) that have the maximum expected future reward given that state
            action = torch.argmax(Q[state]).item()
            new_state, reward, terminated, truncated, info = env.step(action)
            total_rewards_ep += reward
            env.render()

            if terminated or truncated:
                break
            state = new_state
        episode_rewards.append(total_rewards_ep)
    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)

    return mean_reward, std_reward

n_eval_episodes = 10

env = FlappyBirdEnv()
q_table = torch.load("baseline.pth")
mean_reward, std_reward = evaluate_agent(env,n_eval_episodes, q_table)
print(f"Mean_reward={mean_reward:.2f} +/- {std_reward:.2f}")
