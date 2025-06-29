import pygame
import pickle
import numpy as np
from flappy_superhero_env import FlappySuperheroEnv
import time 

# Load trained Q-table
with open("q_table.pkl", "rb") as f:
    q_table = pickle.load(f)

env = FlappySuperheroEnv(render_enabled=True)

# Number of episodes to watch
EPISODES = 10

for episode in range(1, EPISODES + 1):
    state = env.reset()
    done = False
    total_reward = 0
    steps = 0
    done = False
    info = {}

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Choose best action from Q-table
        action = np.argmax(q_table.get(state, np.zeros(2)))
        next_state, reward, done, info = env.step(action)

        state = next_state
        total_reward += reward
        steps += 1
        
    
        # Delay for visibility
        pygame.time.delay(20)
    print(f"Episode {episode}/{EPISODES} | Reward: {total_reward:.2f} | Score: {env.score} | Steps: {steps}")
 
    if info.get("win") :
        font = pygame.font.SysFont(None, 48)
        message = font.render("Congratulations!", True, (50, 20, 0))
        env.screen.blit(message, (env.WIDTH // 2 - 140, env.HEIGHT // 2 + 50))
        pygame.display.flip()
        pygame.time.delay(3000)
        break
            



#pygame.quit()
