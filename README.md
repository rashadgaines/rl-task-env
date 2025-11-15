# Task Management RL Environment

A production-ready Reinforcement Learning training environment designed for training computer-use agents. This full-stack application features comprehensive task validation, programmatic reward systems, and complete API integration.

[![Stack](https://img.shields.io/badge/Stack-Full--Stack-blue?style=for-the-badge)](.)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](.)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](.)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)](.)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](.)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

## Overview

This environment provides 24 programmatically validated RL tasks across 4 difficulty levels, enabling autonomous agent training through a REST API. The system includes a React frontend for visualization, FastAPI backend for agent interaction, and comprehensive validation logic for reward calculation.

**Key Features:**
- 24 RL tasks with programmatic validation (Easy → Medium → Hard → Very Hard)
- Full REST API with state observation and action execution
- Responsive web interface for monitoring and interaction
- Docker containerization for reproducible deployment
- Example agent demonstrating autonomous training
- 585 total reward points across progressive difficulty tiers

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Ports 3000 (frontend) and 8000 (backend) available

### Launch

```bash
docker compose up --build
```

Access the application:
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## Architecture

### Backend

**Stack:** Python 3.11, FastAPI, SQLAlchemy, SQLite

**Core Components:**
- RESTful API with OpenAPI documentation
- Pydantic models for type safety
- SQLAlchemy ORM for database operations
- RL validation system with reward calculation
- Mock data generation using Faker

**API Endpoints:**
```
GET    /api/tasks              # Get all tasks (with filtering)
GET    /api/tasks/{id}         # Get specific task
POST   /api/tasks              # Create new task
PUT    /api/tasks/{id}         # Update task
DELETE /api/tasks/{id}         # Delete task

GET    /api/rl/state           # Get RL environment state
GET    /api/rl/tasks           # Get available RL tasks
POST   /api/rl/validate/{name} # Validate task completion
POST   /api/rl/reset           # Reset environment
```

### Frontend

**Stack:** React 18, Lucide Icons, Axios

**Components:**
- Task board with Kanban-style columns
- RL dashboard with metrics and validation
- Task detail views with inline editing
- Real-time state updates

## RL Training Tasks

The environment includes 24 programmatically validated tasks spanning multiple difficulty levels:

### Easy Tasks (10-20 points)
| Task | Reward | Description |
|------|--------|-------------|
| `create_urgent_task` | 10 | Create a task with urgent priority |
| `complete_three_tasks` | 15 | Mark at least 3 tasks as completed |
| `assign_all_tasks` | 15 | Assign all unassigned tasks |
| `archive_completed` | 15 | Archive all completed tasks |
| `documentation_complete` | 20 | Complete all documentation tasks |

### Medium Tasks (20-25 points)
| Task | Reward | Description |
|------|--------|-------------|
| `organize_by_priority` | 20 | Ensure all high-priority tasks are active |
| `organize_with_tags` | 20 | Add 2+ tags to all tasks |
| `prioritize_urgent_items` | 20 | All urgent tasks must be in progress |
| `reduce_wip` | 20 | Limit work-in-progress to 5 tasks |
| `quality_assurance` | 20 | Add QA tags to completed tasks |
| `balance_workload` | 25 | Distribute tasks evenly across team |
| `clear_overdue_tasks` | 25 | Complete/delete overdue tasks |
| `eliminate_technical_debt` | 25 | Resolve all refactor tasks |
| `deadline_management` | 25 | Manage tasks due within 3 days |
| `no_low_priority_in_progress` | 25 | Optimize priority management |

### Hard Tasks (30-35 points)
| Task | Reward | Description |
|------|--------|-------------|
| `achieve_80_completion` | 30 | Reach 80% completion rate |
| `create_sprint_backlog` | 30 | Create 5+ sprint tasks |
| `optimize_task_flow` | 30 | Balance pipeline (todo < progress < done) |
| `feature_completion` | 30 | Complete all feature tasks |
| `achieve_zero_bugs` | 35 | Resolve all bug tasks |
| `perfect_organization` | 35 | All tasks fully organized |

### Very Hard Tasks (40-50 points)
| Task | Reward | Description |
|------|--------|-------------|
| `team_collaboration` | 40 | Every member has tasks in all statuses |
| `milestone_achievement` | 40 | Complete 10+ tasks in single episode |
| `clean_slate` | 50 | Archive everything - achieve clean board |

**Total Possible Rewards:** 585 points

See [RL_TASKS.md](./RL_TASKS.md) for detailed task documentation and validation criteria.

## Agent Integration

### Example Agent

Run the included example agent to see autonomous interaction:

```bash
# Start environment
docker compose up --build

# In a new terminal
python3 -m venv venv
source venv/bin/activate
pip install -r agent-requirements.txt
python3 example_agent.py
```

### Training with RL Frameworks

The environment supports integration with standard RL frameworks:
- Stable Baselines3 (PPO, DQN, A2C)
- RLlib (Ray)
- OpenAI Gym
- Anthropic Computer Use API

See [AGENT_INTEGRATION.md](./AGENT_INTEGRATION.md) for:
- Complete integration examples
- OpenAI Gym wrapper implementation
- State/action space design
- Reward shaping strategies
- Multi-agent training setup

### Quick Integration

```python
import requests

# Observe state
state = requests.get("http://localhost:8000/api/rl/state").json()

# Take action
requests.put("http://localhost:8000/api/tasks/1", 
             json={"status": "completed"})

# Validate and get reward
result = requests.post(
    "http://localhost:8000/api/rl/validate/complete_three_tasks"
).json()

print(f"Reward: {result['reward']}")  # 15.0
```

## Environment State

The environment exposes comprehensive state information for agent observation:

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

## Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API documentation available at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm start
```

### Environment Variables

**Backend:**
```env
DATABASE_URL=sqlite:////data/tasks.db
PYTHONUNBUFFERED=1
```

**Frontend:**
```env
REACT_APP_API_URL=http://localhost:8000
```

## Documentation

- [SETUP.md](./SETUP.md) - Detailed setup instructions and troubleshooting
- [RL_TASKS.md](./RL_TASKS.md) - Complete task guide with validation details
- [AGENT_INTEGRATION.md](./AGENT_INTEGRATION.md) - Agent training and integration
- [AGENT_TRAINING_FLOW.md](./AGENT_TRAINING_FLOW.md) - Visual training explanation

## License

MIT License - See [LICENSE](./LICENSE) for details.
