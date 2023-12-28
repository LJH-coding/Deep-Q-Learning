import pygame, random, time, sys
# 參數設定
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

class Environment:
    def __init__(self):
        # 建立遊戲視窗
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        pygame.mixer.init()
        # 載入資料
        self.bg_surface = pygame.image.load("./assets/img/background-day.png").convert()
        self.floor_surface = pygame.image.load("./assets/img/base.png").convert()
        self.bird_surface = [pygame.image.load("./assets/img/bluebird-downflap.png").convert(), pygame.image.load("./assets/img/bluebird-midflap.png").convert(), pygame.image.load("./assets/img/bluebird-upflap.png").convert()]
        self.pipe_surface = pygame.image.load("./assets/img/pipe-green.png").convert()
        self.begin_surface = pygame.image.load("./assets/img/message.png").convert_alpha()
        self.gameover_surface = pygame.image.load("./assets/img/gameover.png").convert_alpha()
        self.point_sound = pygame.mixer.Sound("./assets/audio/point.ogg")
        self.point_sound.set_volume(0.2)
        # 位置設定
        self.bird_rect = self.bird_surface[0].get_rect(center = (50, SCREEN_HEIGHT // 2))
        self.floor_x_pos = 0
        self.bird_velocity = 0
        self.pipe_list = []
        self.point = 0
        self.bird_index = 0
        self.counter = 0
        self.done = False
        self.gravity = 0.25
        self.gamespeed = 3.5
        
    def reset(self):
        self.point = 0
        self.bird_index = 0
        self.counter = 0
        self.done = False
        self.bird_velocity = 0
        self.pipe_list = []
        self.bird_rect = self.bird_surface[0].get_rect(center = (50, SCREEN_HEIGHT // 2))
        self.floor_x_pos = 0
        self.reward_base = 0.1
        self.target = 10

    def get_state(self):
        state = []
        if len(self.pipe_list) == 0:
            state.append(1)
            state.append(1)
            state.append(1)
            state.append(1)
            state.append(0)
            state.append(0)
        else:
            state.append(int(self.bird_rect.centery < self.pipe_list[0].top)) #upper than bottom_pipe top
            state.append(int(self.bird_rect.centery > self.pipe_list[1].bottom)) #lower than top_pipe top
            state.append(int(self.bird_rect.centery < self.pipe_list[0].top - 50)) #upper than bottom_pipe top
            state.append(int(self.bird_rect.centery > self.pipe_list[1].bottom + 50)) #lower than top_pipe top
            state.append(int(self.pipe_list[0].left - self.bird_rect.right < 100))
            state.append(int(self.pipe_list[0].left - self.bird_rect.right < 50))

        state.append(int(self.bird_velocity > 0))
        return tuple(state)

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

        if self.point == self.target:
            self.gamespeed = self.gamespeed + 0.1
            self.target += 10
            self.reward_base += 0.1

        reward = self.reward_base
        #update
        self.bird_velocity = self.bird_velocity + self.gravity
        self.bird_rect.centery = self.bird_rect.centery + self.bird_velocity # bird_rect.center 代表鳥的位置
        #picture index
        self.bird_index = (self.bird_index + (self.counter == 5)) % 3
        self.counter = (self.counter + 1) % 6;
        #pipe
        self.pipe_update()

        if len(self.pipe_list) == 0:
            self.point += 1
            reward = 1

        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe) == True:
                reward = -10
                self.done = True

        if self.bird_rect.top <= 0 or self.bird_rect.bottom >= 450:
            reward = -10
            self.done = True
        
        return self.get_state(), reward, self.done

    def render(self):
        #draw
        self.screen.blit(self.bg_surface, (0, 0))
        self.screen.blit(self.bird_surface[self.bird_index], self.bird_rect)
        for pipe in self.pipe_list:
            if pipe.bottom >= 450:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

        # 地板移動
        self.floor_x_pos -= self.gamespeed
        if self.floor_x_pos <= -SCREEN_WIDTH:
            self.floor_x_pos = 0    
        self.screen.blit(self.floor_surface, (self.floor_x_pos, 450))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + SCREEN_WIDTH, 450))
        
        # 更新畫面
        pygame.display.update()
        pygame.time.Clock().tick(60)

    def run(self):
        action = 0
        # 遊戲迴圈
        while True:
            # 取得使用者輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                try:
                    if(event.text == ' '):
                        action = 1
                except:
                    continue

            state, reward, done = self.step(action)
            action = 0

            self.render()

            if done:
                break

#Game = Environment()
#Game.run()

