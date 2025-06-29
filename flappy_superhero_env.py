import pygame
import random
import numpy as np
import os

class FlappySuperheroEnv:
    def __init__(self, render_enabled=False):
        pygame.init()
        self.WIDTH = 288
        self.HEIGHT = 512
        self.PIPE_WIDTH = 52
        self.PIPE_HEIGHT = 320
        self.PIPE_GAP = 100
        self.BIRD_WIDTH = 34
        self.BIRD_HEIGHT = 24
        self.GRAVITY = 1
        self.FLAP_STRENGTH = -10
        self.VELOCITY_MAX = 10
        self.render_enabled = render_enabled
        
        if self.render_enabled:
            pygame.font.init()
            self.font = pygame.font.SysFont(None, 36)
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Flappy Superhero")
            self.clock = pygame.time.Clock()
            
            # Load assets
            path = os.path.join(os.path.dirname(__file__), "assets")
            self.bg = pygame.transform.scale(pygame.image.load(os.path.join(path, "background.png")), (self.WIDTH, self.HEIGHT))
            self.bird_img = pygame.transform.scale(pygame.image.load(os.path.join(path, "superhero.png")), (self.BIRD_WIDTH, self.BIRD_HEIGHT))
            self.coin_img = pygame.transform.scale(pygame.image.load(os.path.join(path, "coin.png")), (30, 30))

        self.reset()

    def reset(self):
        self.bird_y = self.HEIGHT // 2
        self.velocity = 0
        self.pipe_x = self.WIDTH + 100
        self.pipe_y = random.randint(50, self.HEIGHT - 150)
        self.score = 0
        self.done = False
        self.coin_active = False
        self.coin_collected = False
        self.coin_x = None
        self.coin_y = None
        
        return self.get_state()

    def step(self, action):
        reward = 0
        
        if action == 1:
            self.velocity = self.FLAP_STRENGTH

        self.velocity = min(self.velocity + self.GRAVITY, self.VELOCITY_MAX)
        self.bird_y += self.velocity

        self.pipe_x -= 4
        reward += 1
        
        if self.pipe_x < -self.PIPE_WIDTH:
            self.pipe_x = self.WIDTH
            self.pipe_y = random.randint(50, self.HEIGHT - 150)
            self.score += 1
            reward += 100
            
            if self.score == 10 and not self.coin_active:
                self.coin_active = True
                self.coin_collected = False
                self.coin_x = self.pipe_x + self.PIPE_WIDTH // 2  # Place it between pipes
                self.coin_y = self.pipe_y + self.PIPE_GAP // 2  
        
        if self.coin_active and not self.coin_collected:
            self.coin_x -= 4
            
        # Bonus reward for getting close to pipe center 
        gap_center = self.pipe_y + self.PIPE_GAP / 2
        distance = abs(gap_center - self.bird_y)
        reward += max(0, 5 - distance / 10)

        if self.check_collision():
            self.done = True
            reward = -1000
         
        if self.coin_active and not self.coin_collected:
            coin_rect = pygame.Rect(self.coin_x, self.coin_y, 30, 30)
            bird_rect = pygame.Rect(50, self.bird_y, self.BIRD_WIDTH, self.BIRD_HEIGHT)
            
            if bird_rect.colliderect(coin_rect):
                self.coin_collected = True
                self.done = True
                reward += 1000  # bonus for collecting the coin 
                return self.get_state(), reward, self.done, {"win": True}


        if self.render_enabled:
            self.render()
        return self.get_state(), reward, self.done, {}
       
      

    def check_collision(self):
        in_pipe_range = self.pipe_x < 50 < self.pipe_x + self.PIPE_WIDTH
        pipe_top = self.pipe_y
        pipe_bottom = self.pipe_y + self.PIPE_GAP
        hit_pipe = in_pipe_range and not (pipe_top < self.bird_y < pipe_bottom)
        hit_ground = self.bird_y > self.HEIGHT or self.bird_y < 0
        return hit_pipe or hit_ground

    def get_state(self):
        x_dist = self.pipe_x - 50  # horizontal distance from bird to pipe
        y_dist = self.pipe_y + self.PIPE_GAP / 2 - self.bird_y  # vertical distance to gap center
        vel = self.velocity
        alive = int(not self.done)
        return( 
            min(20, max(0, x_dist // 15)),
            min(20, max(-20, int(y_dist // 10))),
            min(10, max(-10, vel))
        )
        

    def render(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.bird_img, (50, self.bird_y))

        # Pipes
        pygame.draw.rect(self.screen, (0, 255, 0), (self.pipe_x, 0, self.PIPE_WIDTH, self.pipe_y))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.pipe_x, self.pipe_y + self.PIPE_GAP, self.PIPE_WIDTH, self.HEIGHT))
        
        #coins
        if self.coin_active and not self.coin_collected:
            self.screen.blit(self.coin_img, (self.coin_x, self.coin_y))
            
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        
            
        # win game 
        if self.done and self.coin_collected:
            win_text = self.font.render("YOU WIN!", True, (255, 215, 0))
            self.screen.blit(win_text, (self.WIDTH // 2 - 80, self.HEIGHT // 2))

        pygame.display.flip()
        self.clock.tick(30)
