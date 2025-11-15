# Agent Integration Guide

Complete guide for integrating RL agents with the Task Management environment.

## Overview

Agents interact with the environment through a REST API:
1. Observe state via GET requests
2. Execute actions via PUT/POST/DELETE requests
3. Validate goals and receive rewards
4. Learn from experience and iterate

## Quick Start

Run the included example agent:

```bash
docker compose up --build  # Start environment
python3 -m venv venv
source venv/bin/activate
pip install -r agent-requirements.txt
python3 example_agent.py
```

## Integration Methods

### Method 1: Direct API Integration

For custom RL implementations or computer-use agents:

```python
import requests

class TaskAgent:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
    
    def observe(self):
        response = requests.get(f"{self.api_url}/api/rl/state")
        return response.json()
    
    def act(self, action):
        if action["type"] == "update_status":
            requests.put(
                f"{self.api_url}/api/tasks/{action['task_id']}",
                json={"status": action["status"]}
            )
        elif action["type"] == "create_task":
            requests.post(
                f"{self.api_url}/api/tasks",
                json=action["data"]
            )
    
    def get_reward(self, task_name):
        response = requests.post(
            f"{self.api_url}/api/rl/validate/{task_name}"
        )
        return response.json()["reward"]
```

### Method 2: OpenAI Gym Interface

For standard RL libraries (Stable Baselines3, RLlib, etc.):

```python
import gym
import numpy as np
import requests
from gym import spaces

class TaskManagementEnv(gym.Env):
    def __init__(self, api_url="http://localhost:8000"):
        super().__init__()
        self.api_url = api_url
        
        # Define action space: [task_id, action_type, parameter]
        self.action_space = spaces.MultiDiscrete([100, 4, 4])
        
        # Define observation space: [task_count, completion_rate, ...]
        self.observation_space = spaces.Box(
            low=0, high=100, shape=(10,), dtype=np.float32
        )
    
    def reset(self):
        requests.post(f"{self.api_url}/api/rl/reset")
        return self._get_observation()
    
    def step(self, action):
        task_id, action_type, param = action
        
        # Execute action
        if action_type == 0:  # Update status
            self._update_task(task_id, "status", param)
        
        # Get new state
        obs = self._get_observation()
        
        # Calculate reward
        reward = self._get_reward()
        
        # Check if done
        done = self._is_done()
        
        return obs, reward, done, {}
    
    def _get_observation(self):
        state = requests.get(f"{self.api_url}/api/rl/state").json()
        return np.array([
            state["total_tasks"],
            state["completion_rate"],
            state["tasks_by_status"].get("todo", 0),
            state["tasks_by_status"].get("in_progress", 0),
            state["tasks_by_status"].get("completed", 0),
            state["tasks_by_priority"].get("urgent", 0),
            state["tasks_by_priority"].get("high", 0),
            state["tasks_by_priority"].get("medium", 0),
            state["tasks_by_priority"].get("low", 0),
            state["actions_taken"]
        ], dtype=np.float32)
    
    def _update_task(self, task_id, field, value):
        status_map = {0: "todo", 1: "in_progress", 2: "completed", 3: "archived"}
        requests.put(
            f"{self.api_url}/api/tasks/{task_id}",
            json={field: status_map.get(value, value)}
        )
    
    def _get_reward(self):
        total = 0.0
        for task in ["complete_three_tasks", "assign_all_tasks"]:
            try:
                result = requests.post(
                    f"{self.api_url}/api/rl/validate/{task}"
                ).json()
                if result["completed"]:
                    total += result["reward"]
            except:
                pass
        return total
    
    def _is_done(self):
        state = requests.get(f"{self.api_url}/api/rl/state").json()
        return state["completion_rate"] >= 80.0 or state["actions_taken"] >= 50
```

## Training Examples

### Example 1: DQN Agent

```python
import torch
import torch.nn as nn
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.model = DQN(state_size, action_size)
        self.optimizer = torch.optim.Adam(self.model.parameters())
    
    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        with torch.no_grad():
            q_values = self.model(torch.FloatTensor(state))
            return q_values.argmax().item()
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        # Standard DQN training logic here
        if self.epsilon > 0.01:
            self.epsilon *= self.epsilon_decay
```

### Example 2: PPO with Stable Baselines3

```python
from stable_baselines3 import PPO

# Create environment
env = TaskManagementEnv("http://localhost:8000")

# Create PPO agent
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    verbose=1
)

# Train
model.learn(total_timesteps=100000)

# Save
model.save("task_agent")

# Test
obs = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _ = env.step(action)
    if done:
        obs = env.reset()
```

## State and Action Spaces

### State Encoding

Convert API response to neural network input:

```python
def encode_state(state_dict):
    total = state_dict["total_tasks"]
    return np.array([
        total,
        state_dict["completion_rate"] / 100,
        state_dict["tasks_by_status"].get("todo", 0) / total,
        state_dict["tasks_by_status"].get("in_progress", 0) / total,
        state_dict["tasks_by_status"].get("completed", 0) / total,
        state_dict["tasks_by_priority"].get("urgent", 0) / total,
        state_dict["tasks_by_priority"].get("high", 0) / total,
        state_dict["tasks_by_priority"].get("medium", 0) / total,
        state_dict["tasks_by_priority"].get("low", 0) / total,
        min(state_dict["actions_taken"] / 100, 1.0)
    ])
```

### Action Encoding

Map discrete actions to API calls:

```python
actions = {
    0: lambda: update_task_status(1, "completed"),
    1: lambda: update_task_status(2, "in_progress"),
    2: lambda: create_task({"title": "New task", "priority": "urgent"}),
    3: lambda: assign_task(1, "Alice"),
    # ... more actions
}
```

## Reward Shaping

### Direct Rewards

From validation endpoints:

```python
result = requests.post(
    "http://localhost:8000/api/rl/validate/complete_three_tasks"
).json()
reward = result["reward"]  # 15.0 if completed
```

### Custom Reward Function

Add additional reward signals:

```python
def calculate_reward(prev_state, action, new_state):
    reward = 0.0
    
    # Reward for increasing completion rate
    if new_state["completion_rate"] > prev_state["completion_rate"]:
        reward += 0.1
    
    # Penalty for too many actions
    if new_state["actions_taken"] > 50:
        reward -= 0.1
    
    # Bonus for completing RL tasks
    for task_name in RL_TASKS:
        result = validate_task(task_name)
        if result["completed"]:
            reward += result["reward"]
    
    return reward
```

## Multi-Agent Training

Run multiple environments in parallel:

```python
from stable_baselines3.common.vec_env import SubprocVecEnv

def make_env(port):
    def _init():
        return TaskManagementEnv(f"http://localhost:{port}")
    return _init

# Create 4 parallel environments
envs = SubprocVecEnv([make_env(8000 + i) for i in range(4)])

model = PPO("MlpPolicy", envs, verbose=1)
model.learn(total_timesteps=1000000)
```

## Curriculum Learning

Progressive training from easy to hard:

```python
curriculum = [
    ["create_urgent_task", "complete_three_tasks"],  # Easy
    ["assign_all_tasks", "organize_by_priority"],    # Medium
    ["achieve_80_completion", "balance_workload"],   # Hard
    ["team_collaboration", "clean_slate"]            # Very Hard
]

for stage, tasks in enumerate(curriculum):
    print(f"Training stage {stage}")
    env.set_active_tasks(tasks)
    model.learn(total_timesteps=10000)
```

## Monitoring

Track performance with Weights & Biases:

```python
import wandb

wandb.init(project="task-management-rl")

for episode in range(1000):
    state = env.reset()
    episode_reward = 0
    
    while not done:
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        episode_reward += reward
        state = next_state
    
    wandb.log({
        "episode": episode,
        "reward": episode_reward,
        "completion_rate": info["completion_rate"]
    })
```

## Best Practices

1. Start with the example agent to understand the API
2. Normalize state values to [0, 1] range
3. Balance immediate and long-term rewards
4. Use epsilon-greedy or entropy bonuses for exploration
5. Save model checkpoints frequently
6. Monitor metrics with TensorBoard or Weights & Biases
7. Test on held-out task combinations

## Resources

- [Stable Baselines3 Documentation](https://stable-baselines3.readthedocs.io/)
- [OpenAI Gym Tutorial](https://gymnasium.farama.org/)
- [RLlib Documentation](https://docs.ray.io/en/latest/rllib/index.html)
