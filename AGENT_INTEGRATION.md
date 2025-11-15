# 🤖 Agent Integration Guide

This guide explains how to connect actual RL agents to train autonomously in this environment.

## 🎯 Overview

The environment provides a **REST API** that agents interact with. An agent:
1. **Observes** state via API calls
2. **Takes actions** by calling API endpoints
3. **Receives rewards** through validation
4. **Learns** from experience

---

## 🚀 Quick Start: Run the Example Agent

```bash
# 1. Ensure environment is running
docker compose up --build

# 2. Run the example agent
python3 example_agent.py
```

The example agent demonstrates:
- How to connect to the API
- How to observe state
- How to take actions
- How to validate and get rewards

---

## 🔄 The RL Training Loop

### **Standard RL Flow:**

```python
while training:
    # 1. OBSERVE: Get current state
    state = agent.get_state()
    
    # 2. DECIDE: Choose action based on policy
    action = agent.policy(state)
    
    # 3. EXECUTE: Perform action via API
    agent.execute_action(action)
    
    # 4. VALIDATE: Check if goal achieved
    result = agent.validate_rl_task("task_name")
    
    # 5. LEARN: Update policy based on reward
    agent.learn(state, action, result["reward"])
```

### **In This Environment:**

```python
# State: GET /api/rl/state
{
  "total_tasks": 15,
  "tasks_by_status": {"todo": 6, "in_progress": 4, ...},
  "completion_rate": 33.3,
  "actions_taken": 0,
  "current_reward": 0.0
}

# Action: Any API call (CRUD operations)
PUT /api/tasks/5 {"status": "completed"}

# Reward: POST /api/rl/validate/complete_three_tasks
{
  "completed": true,
  "reward": 15.0,
  "feedback": "✅ 3 tasks completed"
}
```

---

## 🔧 Integration Methods

### **Method 1: Direct API Integration** (Simplest)

Perfect for:
- Custom RL implementations
- Computer-use agents (like Anthropic's)
- Browser automation agents

```python
import requests

class TaskAgent:
    def __init__(self):
        self.api_url = "http://localhost:8000"
    
    def observe(self):
        response = requests.get(f"{self.api_url}/api/rl/state")
        return response.json()
    
    def act(self, action):
        if action["type"] == "update_task":
            requests.put(
                f"{self.api_url}/api/tasks/{action['task_id']}",
                json=action["updates"]
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

### **Method 2: OpenAI Gym Interface** (Standard RL)

Perfect for:
- Stable Baselines3
- RLlib
- TensorFlow Agents
- Any Gym-compatible library

```python
import gym
import requests
import numpy as np
from gym import spaces

class TaskManagementEnv(gym.Env):
    """
    OpenAI Gym wrapper for Task Management Environment
    """
    
    def __init__(self, api_url="http://localhost:8000"):
        super().__init__()
        self.api_url = api_url
        
        # Define action space
        # Actions: [task_id, action_type, priority, status]
        self.action_space = spaces.MultiDiscrete([100, 4, 4, 4])
        
        # Define observation space
        # State: [total_tasks, completion_rate, tasks_by_status, ...]
        self.observation_space = spaces.Box(
            low=0, high=100,
            shape=(10,),
            dtype=np.float32
        )
        
        self.current_episode = 0
    
    def reset(self):
        """Reset environment for new episode"""
        requests.post(f"{self.api_url}/api/rl/reset")
        self.current_episode += 1
        return self._get_observation()
    
    def step(self, action):
        """Execute action and return (obs, reward, done, info)"""
        # Parse action
        task_id, action_type, priority, status = action
        
        # Execute action via API
        if action_type == 0:  # Update status
            self._update_task_status(task_id, status)
        elif action_type == 1:  # Update priority
            self._update_task_priority(task_id, priority)
        # ... more action types
        
        # Get new observation
        obs = self._get_observation()
        
        # Calculate reward
        reward = self._calculate_reward()
        
        # Check if episode is done
        done = self._is_episode_done()
        
        info = {}
        
        return obs, reward, done, info
    
    def _get_observation(self):
        """Get state from API and convert to numpy array"""
        response = requests.get(f"{self.api_url}/api/rl/state")
        state = response.json()
        
        # Convert to fixed-size observation vector
        obs = np.array([
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
        
        return obs
    
    def _update_task_status(self, task_id, status_code):
        """Update task status via API"""
        status_map = {0: "todo", 1: "in_progress", 2: "completed", 3: "archived"}
        requests.put(
            f"{self.api_url}/api/tasks/{task_id}",
            json={"status": status_map[status_code]}
        )
    
    def _calculate_reward(self):
        """Calculate reward by validating multiple RL tasks"""
        total_reward = 0.0
        
        # Try validating common tasks
        for task_name in ["complete_three_tasks", "assign_all_tasks"]:
            try:
                result = requests.post(
                    f"{self.api_url}/api/rl/validate/{task_name}"
                ).json()
                if result["completed"]:
                    total_reward += result["reward"]
            except:
                pass
        
        return total_reward
    
    def _is_episode_done(self):
        """Check if episode is complete"""
        state = requests.get(f"{self.api_url}/api/rl/state").json()
        # Episode done if high completion rate or many actions taken
        return (state["completion_rate"] >= 80.0 or 
                state["actions_taken"] >= 50)


# Usage with Stable Baselines3
from stable_baselines3 import PPO

env = TaskManagementEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("task_agent")
```

### **Method 3: Anthropic Computer Use Integration**

Perfect for:
- Claude with computer use
- Agents that interact via UI
- Multi-modal agents

```python
import anthropic

def task_management_tool():
    """
    Tool definition for Claude to interact with environment
    """
    return {
        "name": "task_management",
        "description": "Manage tasks in the RL environment",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_state", "update_task", "create_task", "validate"]
                },
                "task_id": {"type": "integer"},
                "updates": {"type": "object"}
            }
        }
    }

# Use with Claude
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[task_management_tool()],
    messages=[{
        "role": "user",
        "content": "Complete 3 tasks in the task management system"
    }]
)
```

---

## 🎓 Training Examples

### **Example 1: Simple DQN Agent**

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

class TaskDQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = DQN(state_size, action_size)
        self.optimizer = torch.optim.Adam(self.model.parameters())
    
    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        
        with torch.no_grad():
            state = torch.FloatTensor(state)
            q_values = self.model(state)
            return q_values.argmax().item()
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target += self.gamma * self.model(
                    torch.FloatTensor(next_state)
                ).max()
            
            # Train network
            # ... (standard DQN training)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Training loop
env = TaskManagementEnv()
agent = TaskDQNAgent(state_size=10, action_size=100)

for episode in range(1000):
    state = env.reset()
    total_reward = 0
    
    for step in range(100):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        
        agent.remember(state, action, reward, next_state, done)
        agent.replay()
        
        state = next_state
        total_reward += reward
        
        if done:
            break
    
    print(f"Episode {episode}: Reward = {total_reward}")
```

### **Example 2: PPO with Stable Baselines3**

```python
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

# Create environment
env = TaskManagementEnv()

# Validate environment
check_env(env)

# Create PPO agent
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    verbose=1
)

# Train
model.learn(total_timesteps=100000)

# Save
model.save("task_ppo_agent")

# Test
obs = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()
```

---

## 📊 State Space Design

### **What the Agent Observes:**

```python
{
    "total_tasks": int,           # Total number of tasks
    "tasks_by_status": {          # Distribution by status
        "todo": int,
        "in_progress": int,
        "completed": int,
        "archived": int
    },
    "tasks_by_priority": {        # Distribution by priority
        "low": int,
        "medium": int,
        "high": int,
        "urgent": int
    },
    "completion_rate": float,     # Percentage complete
    "actions_taken": int,         # Number of actions in episode
    "current_reward": float,      # Cumulative reward
    "episode_number": int         # Current episode
}
```

### **Encoding for Neural Networks:**

```python
def encode_state(state_dict):
    """Convert API response to neural network input"""
    return np.array([
        state_dict["total_tasks"],
        state_dict["completion_rate"] / 100,  # Normalize
        state_dict["tasks_by_status"].get("todo", 0) / state_dict["total_tasks"],
        state_dict["tasks_by_status"].get("in_progress", 0) / state_dict["total_tasks"],
        state_dict["tasks_by_status"].get("completed", 0) / state_dict["total_tasks"],
        state_dict["tasks_by_priority"].get("urgent", 0) / state_dict["total_tasks"],
        state_dict["tasks_by_priority"].get("high", 0) / state_dict["total_tasks"],
        state_dict["tasks_by_priority"].get("medium", 0) / state_dict["total_tasks"],
        state_dict["tasks_by_priority"].get("low", 0) / state_dict["total_tasks"],
        min(state_dict["actions_taken"] / 100, 1.0),  # Normalize
    ])
```

---

## 🎯 Action Space Design

### **Possible Actions:**

1. **Update Task Status** (task_id, new_status)
2. **Update Task Priority** (task_id, new_priority)
3. **Assign Task** (task_id, assignee)
4. **Add Tags** (task_id, tags)
5. **Create Task** (task_data)
6. **Delete Task** (task_id)

### **Action Encoding:**

```python
# Discrete action space
actions = {
    0: lambda: update_task_status(task_id=1, status="completed"),
    1: lambda: update_task_status(task_id=2, status="in_progress"),
    2: lambda: create_urgent_task(),
    3: lambda: assign_task(task_id=1, assignee="Alice"),
    # ... up to N actions
}

# Or continuous action space
action_vector = [
    task_id,          # Which task (0-1 normalized)
    action_type,      # What to do (0-1, mapped to discrete actions)
    parameter_1,      # Action-specific parameter
    parameter_2,      # Action-specific parameter
]
```

---

## 💰 Reward Shaping

### **Direct Rewards (from validation):**

```python
POST /api/rl/validate/complete_three_tasks
→ {"reward": 15.0, "completed": true}
```

### **Custom Reward Shaping:**

```python
def calculate_reward(prev_state, action, new_state):
    """
    Custom reward function beyond task validation
    """
    reward = 0.0
    
    # Reward for completing tasks
    if new_state["completion_rate"] > prev_state["completion_rate"]:
        reward += (new_state["completion_rate"] - prev_state["completion_rate"]) * 0.1
    
    # Penalty for too many actions
    if new_state["actions_taken"] > 50:
        reward -= 0.1
    
    # Bonus for completing RL tasks
    for task_name in RL_TASKS:
        result = validate_rl_task(task_name)
        if result["completed"]:
            reward += result["reward"]
    
    return reward
```

---

## 🚀 Advanced Integration

### **Multi-Agent Training:**

```python
# Run multiple environments in parallel
from stable_baselines3.common.vec_env import SubprocVecEnv

def make_env(port):
    def _init():
        return TaskManagementEnv(f"http://localhost:{port}")
    return _init

# Create parallel environments (need multiple backend instances)
envs = SubprocVecEnv([make_env(8000 + i) for i in range(4)])

model = PPO("MlpPolicy", envs, verbose=1)
model.learn(total_timesteps=1000000)
```

### **Curriculum Learning:**

```python
# Start with easy tasks, progress to hard
curriculum = [
    ["create_urgent_task", "complete_three_tasks"],  # Easy
    ["assign_all_tasks", "organize_by_priority"],    # Medium
    ["achieve_80_completion", "balance_workload"],   # Hard
    ["team_collaboration", "clean_slate"]            # Very Hard
]

for stage, tasks in enumerate(curriculum):
    print(f"Training on stage {stage}")
    env.set_active_tasks(tasks)
    model.learn(total_timesteps=10000)
```

---

## 📈 Monitoring & Evaluation

### **Track Performance:**

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
    
    # Log metrics
    wandb.log({
        "episode": episode,
        "reward": episode_reward,
        "completion_rate": info["completion_rate"],
        "actions_taken": info["actions_taken"]
    })
```

---

## 🎯 Best Practices

1. **Start Simple**: Use the example agent to understand the API
2. **Validate Environment**: Check that rewards make sense
3. **Normalize Inputs**: Scale state values to [0, 1]
4. **Reward Shaping**: Balance immediate vs long-term rewards
5. **Exploration**: Use epsilon-greedy or entropy bonuses
6. **Checkpointing**: Save models frequently
7. **Monitoring**: Track metrics with TensorBoard/Weights & Biases
8. **Testing**: Evaluate on held-out task combinations

---

## 🔗 Resources

- **Stable Baselines3**: https://stable-baselines3.readthedocs.io/
- **OpenAI Gym**: https://gymnasium.farama.org/
- **RLlib**: https://docs.ray.io/en/latest/rllib/index.html
- **Anthropic Computer Use**: https://www.anthropic.com/

---

**Ready to train your agent!** Start with `example_agent.py` and progress to full RL implementations. 🚀

