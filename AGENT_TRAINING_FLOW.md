# Agent Training Flow

## Overview

Agents connect via REST API and train autonomously through observation, action, and reward cycles.

## Training Loop

```
Agent observes STATE          → GET /api/rl/state
Agent decides ACTION           → Policy/neural network determines move
Agent executes via API         → PUT/POST/DELETE /api/tasks/...
Agent validates REWARD         → POST /api/rl/validate/{task_name}
Agent learns from experience   → Update neural network weights
Repeat                         → Continue for thousands of iterations
```

## Example Training Flow

### Goal: Train agent to complete 3 tasks

```python
import requests

while training:
    # 1. Observe environment
    state = requests.get("http://localhost:8000/api/rl/state").json()
    # Returns: {completion_rate: 20%, total_tasks: 15, ...}
    
    # 2. Decide action (neural network or policy)
    action = agent.policy(state)
    
    # 3. Execute action
    requests.put("http://localhost:8000/api/tasks/5",
                 json={"status": "completed"})
    
    # 4. Validate goal achievement
    result = requests.post(
        "http://localhost:8000/api/rl/validate/complete_three_tasks"
    ).json()
    
    # 5. Learn from reward
    if result["completed"]:
        agent.update_policy(reward=result["reward"])  # +15 points
```

## State Space

What the agent observes:

```json
{
  "total_tasks": 15,
  "tasks_by_status": {
    "todo": 6,
    "in_progress": 4,
    "completed": 3,
    "archived": 2
  },
  "tasks_by_priority": {
    "low": 4,
    "medium": 7,
    "high": 3,
    "urgent": 1
  },
  "completion_rate": 33.3,
  "actions_taken": 42,
  "current_reward": 75.0,
  "episode_number": 1
}
```

## Action Space

Available agent actions:
- Update task status (PUT /api/tasks/{id})
- Change task priority
- Assign task to team member
- Add tags
- Create new task (POST /api/tasks)
- Delete task (DELETE /api/tasks/{id})

## Reward Structure

Rewards by difficulty:
- Easy tasks: 10-20 points
- Medium tasks: 20-25 points
- Hard tasks: 30-35 points
- Very Hard tasks: 40-50 points

Total possible: 585 points

## Integration Methods

### 1. Direct API (Custom RL Code)

```python
import requests

class Agent:
    def observe(self):
        return requests.get("http://localhost:8000/api/rl/state").json()
    
    def act(self, action):
        requests.put(f"http://localhost:8000/api/tasks/{action['id']}",
                     json=action['updates'])
    
    def get_reward(self, task_name):
        result = requests.post(
            f"http://localhost:8000/api/rl/validate/{task_name}"
        ).json()
        return result['reward']
```

### 2. OpenAI Gym (Standard RL)

```python
import gym
from stable_baselines3 import PPO

# Create environment wrapper
env = TaskManagementEnv("http://localhost:8000")

# Train agent
agent = PPO("MlpPolicy", env)
agent.learn(total_timesteps=100000)
```

### 3. Anthropic Computer Use

```python
# Claude interacts via UI
client.messages.create(
    model="claude-3-5-sonnet-20241022",
    tools=[task_management_tool()],
    messages=[{
        "role": "user",
        "content": "Complete 3 tasks in the system"
    }]
)
```

## Training Progression

### Before Training
Random actions, minimal rewards:
```
Episode 1:   Reward: 10   (random exploration)
Episode 10:  Reward: 35   (discovering basics)
```

### After Training
Strategic actions, optimal rewards:
```
Episode 100:  Reward: 245  (mastering easy tasks)
Episode 1000: Reward: 550  (near-optimal policy)
```

## Progressive Learning

### Stage 1: Easy Tasks
Agent learns basic API interaction and task manipulation.
Tasks: `create_urgent_task`, `complete_three_tasks`

### Stage 2: Medium Tasks
Agent learns strategic planning and resource allocation.
Tasks: `organize_by_priority`, `balance_workload`

### Stage 3: Hard Tasks
Agent learns multi-step reasoning and optimization.
Tasks: `achieve_80_completion`, `optimize_task_flow`

### Stage 4: Very Hard Tasks
Agent masters multi-agent coordination and complex constraints.
Tasks: `team_collaboration`, `clean_slate`

## Key Advantages

- REST API enables any agent framework
- Stateless design supports parallel training
- Docker ensures consistent environments
- Programmatic validation requires no human labeling
- 24 diverse tasks provide rich training signal
- Progressive difficulty enables curriculum learning

## Quick Start

1. Start environment: `docker compose up --build`
2. Run example agent: `python3 example_agent.py`
3. Observe behavior in browser at http://localhost:3000
4. Implement your RL algorithm
5. Train and evaluate

See [AGENT_INTEGRATION.md](./AGENT_INTEGRATION.md) for complete code examples and integration guides.
