## Reinforcement Learning with Q-Learning - Flappy Superhero ##

This project combines game development and artificial intelligence.
I built a custom Flappy Bird–style game called Flappy Superhero using Python and Pygame, and then trained an AI agent to play it using Q-learning (a reinforcement learning algorithm).

🔗 Repository: Flappy Superhero RL
🎥 Demo Video: Watch the AI Play

# Project Highlights

# Custom Game Environment:
Designed from scratch in Python with Pygame, structured like an OpenAI Gym environment.

# Reinforcement Learning Agent:
Implemented tabular Q-learning to train the superhero to avoid pipes, survive longer, and eventually win the game.

# Reward System:
> +1 for staying alive
> +100 for passing a pipe
> +5 proximity bonus for precision
> +1000 for collecting the final coin (winning)
> -1000 penalty for crashing

# Game Objective:
Stay alive, pass pipes, and collect the special coin at 10 points to win.

# Tech Stack
- Python (core programming)
- Pygame (game environment)
- NumPy & Pickle (Q-table management & saving progress)

# Training Setup

- Episodes: 50,000
- Discount Factor (γ): 0.99
- Learning Rate (α): adaptive, min 0.01
- Exploration (ε): decayed from 1.0 → 0.05 exponentially

# How to Run ?

# Clone the repository
git clone https://github.com/khadijayadi/flappy-superhero-rl.git
cd flappy-superhero-rl

# Install dependencies
pip install -r requirements.txt

# Play the game manually
python flappy_superhero_env.py

# Train the agent
python q_learning_agent.py

# Watch the trained agent play
python play_with_agent.py


# Attached files explaination :

- the flappy_superhero_env.py : contains the class envirenment of the game.

- the q_learning_agent.py : containt the training logic for the agent and if you run it , it will create a q_table with the training results .
  
- the play_with_agent.py : Here you can see the agent palying the game until he wins based on the previous saved q table .
  
- the plot_metrics.py : containts plots of the game's rewards and scores evolution , it shows how is the training process going .

Run play_with_agent.py without running q_learning_agent.py to see the trained agent play the game using the saved Q-table. 

