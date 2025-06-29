import numpy as np
import matplotlib.pyplot as plt

# Load data
rewards = np.load("training_rewards.npy")
scores = np.load("training_scores.npy")

# Total Reward 
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(rewards, label="Reward", color="tab:blue")
plt.yscale("symlog", linthresh=100)  # Log-like scale for wide reward ranges
plt.title("Episode Rewards ")
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.grid(True)
plt.legend()

# Score per Episode 
plt.subplot(1, 2, 2)
plt.plot(scores, label="Pipes Passed", color="tab:green")
plt.yscale("log")  # Log scale to track long-term improvements
plt.title("Score per Episode ")
plt.xlabel("Episode")
plt.ylabel("Score")
plt.grid(True)
plt.legend()

# save both in the same file 
plt.tight_layout()
plt.savefig("training_curves_log_scaled.png")
plt.show()
