import numpy as np
import pickle
import os
from flappy_superhero_env import FlappySuperheroEnv

# Paths
q_table_path = "q_table.pkl"
rewards_path = "training_rewards.npy"
scores_path = "training_scores.npy"

# Hyperparameters
EPISODES = 50000
GAMMA = 0.99
ALPHA = 0.01
EPSILON_START = 1.0
EPSILON_MIN = 0.05
DECAY_RATE = 0.00005

# Q-table and visit counter
q_table = {}
visit_counts = {}

# Load existing Q-table if it exists
if os.path.exists(q_table_path):
    with open(q_table_path, "rb") as f:
        q_table = pickle.load(f)
    print(" Loaded existing Q-table.")
else:
    print(" Initialized new Q-table.")

all_rewards = []
all_scores = []


# Training loop
for episode in range(1, EPISODES + 1):
    env = FlappySuperheroEnv(render_enabled=False)
    state = env.reset()
    done = False
    epsilon = max(EPSILON_MIN, EPSILON_START * np.exp(-DECAY_RATE * episode))
    total_reward = 0

    while not done:
        # Init state in Q-table if not exists
        if state not in q_table:
            q_table[state] = np.zeros(2)

        # Epsilon-greedy action selection
        if np.random.rand() < epsilon:
            action = np.random.choice(2)
        else:
            action = np.argmax(q_table[state])

        # Environment step
        next_state, reward, done, _ = env.step(action)
        total_reward += reward

        # Init next state
        if next_state not in q_table:
            q_table[next_state] = np.zeros(2)

        # Update Q-value
        sa_pair = (state, action)
        visit_counts[sa_pair] = visit_counts.get(sa_pair, 0) + 1
        alpha = max(ALPHA, 1 / (1 + visit_counts[sa_pair]))

        q_current = q_table[state][action]
        q_target = reward + GAMMA * np.max(q_table[next_state])
        q_table[state][action] = min(10000, q_current + alpha * (q_target - q_current))

        state = next_state

    all_rewards.append(total_reward)
    all_scores.append(env.score)
    

    # Logging
    if episode % 100 == 0:
        print(f"Episode {episode}/{EPISODES} | Reward: {total_reward:.2f} | Epsilon: {epsilon:.3f}")

    # Save checkpoint each 1000 episodes 
    if episode % 1000 == 0:
        with open(q_table_path, "wb") as f:
            pickle.dump(q_table, f)
        np.save(rewards_path, np.array(all_rewards))
        np.save(scores_path, np.array(all_scores))
        

# Final save
with open(q_table_path, "wb") as f:
    pickle.dump(q_table, f)
np.save(rewards_path, np.array(all_rewards))
np.save(scores_path, np.array(all_scores))


