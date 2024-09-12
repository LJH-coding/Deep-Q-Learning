import gymnasium as gym
from gymnasium import spaces
import pygame
import random
import numpy as np
import sys
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

class FlappyBirdEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        super(FlappyBirdEnv, self).__init__()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Discrete(128)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        # Load images
        self.bg_surface = pygame.image.load("./assets/img/background-day.png").convert()
        self.floor_surface = pygame.image.load("./assets/img/base.png").convert()
        self.bird_surface = [pygame.image.load("./assets/img/bluebird-downflap.png").convert(), pygame.image.load("./assets/img/bluebird-midflap.png").convert(), pygame.image.load("./assets/img/bluebird-upflap.png").convert()]
        self.pipe_surface = pygame.image.load("./assets/img/pipe-green.png").convert()
        self.begin_surface = pygame.image.load("./assets/img/message.png").convert_alpha()
        self.gameover_surface = pygame.image.load("./assets/img/gameover.png").convert_alpha()

        self.reset()

    def reset(self, seed=0, options=0):
        # Reset the game state
        self.bird_rect = self.bird_surface[0].get_rect(center=(50, SCREEN_HEIGHT // 2))
        self.bird_velocity = 0
        self.pipe_list = []
        self.point = 0
        self.done = False
        self.gravity = 0.25
        self.gamespeed = 3.5
        self.counter = 0
        self.floor_x_pos = 0
        state = self.get_state()
        return state, {}

    def get_state(self):
        if len(self.pipe_list) == 0:
            state = [1, 1, 1, 1, 0, 0]
        else:
            state = [
                int(self.bird_rect.centery < self.pipe_list[0].top),
                int(self.bird_rect.centery > self.pipe_list[1].bottom),
                int(self.bird_rect.centery < self.pipe_list[0].top - 50),
                int(self.bird_rect.centery > self.pipe_list[1].bottom + 50),
                int(self.pipe_list[0].left - self.bird_rect.right < 100),
                int(self.pipe_list[0].left - self.bird_rect.right < 50)
            ]
        state.append(int(self.bird_velocity > 0))
        return int(''.join(map(str, state)), 2)

    def pipe_update(self):
        if len(self.pipe_list) == 0:
            random_pipe_pos = random.choice([100, 130, 150, 160, 170, 200, 250, 300, 330])
            bottom_pipe = self.pipe_surface.get_rect(midtop = (SCREEN_WIDTH + 100, SCREEN_HEIGHT - random_pipe_pos))
            top_pipe = self.pipe_surface.get_rect(midbottom = (SCREEN_WIDTH + 100, SCREEN_HEIGHT - random_pipe_pos - 150))
            self.pipe_list = [bottom_pipe, top_pipe]
        else:
            for pipe in self.pipe_list:
                pipe.centerx -= self.gamespeed
                if pipe.right <= 0:
                    self.pipe_list = []

    def step(self, action = 0):
        if action == 0:
            self.bird_velocity = self.bird_velocity
        else:
            self.bird_velocity = -6.5

        reward = 0.1
        #update
        self.bird_velocity += self.gravity
        self.bird_rect.centery += self.bird_velocity
        #pipe
        self.pipe_update()

        if len(self.pipe_list) == 0:
            self.point += 1
            reward = 1

        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe) == True:
                self.done = True

        if self.bird_rect.top <= 0 or self.bird_rect.bottom >= 450:
            self.done = True
        
        if self.done:
            reward = -10
        
        return self.get_state(), reward, self.done, False, {}

    def render(self):
        #draw
        self.screen.blit(self.bg_surface, (0, 0))
        self.counter = (self.counter + 1) % 18
        self.screen.blit(self.bird_surface[self.counter // 6], self.bird_rect)
        for pipe in self.pipe_list:
            if pipe.bottom >= 450:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

        self.floor_x_pos -= self.gamespeed
        if self.floor_x_pos <= -SCREEN_WIDTH:
            self.floor_x_pos = 0    
        self.screen.blit(self.floor_surface, (self.floor_x_pos, 450))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + SCREEN_WIDTH, 450))
        
        pygame.display.update()
        pygame.time.Clock().tick(60)

    def run(self):
        action, re = 0, 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                try:
                    if(event.text == ' '):
                        action = 1
                except:
                    continue

            state, reward, terminated, truncated, _ = self.step(action)
            action = 0
            re += reward

            self.render()

            if terminated or truncated:
                print("return: ", re)
                re = 0
                self.reset()

    def close(self):
        pygame.quit()

if __name__ == "__main__":
    env = FlappyBirdEnv()
    print(env.action_space)
    print(env.observation_space)

    env.run()
