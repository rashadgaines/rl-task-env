# 🎯 Task Management RL Environment

A production-ready **Reinforcement Learning Training Environment** designed for training computer-use agents. This full-stack application demonstrates comprehensive skills in containerization, frontend design, backend development, database management, and RL paradigm understanding.

[![Stack](https://img.shields.io/badge/Stack-Full--Stack-blue?style=for-the-badge)](.)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](.)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](.)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)](.)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](.)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

> **🚀 One Command Setup:** `docker compose up --build`  
> **🎮 24 RL Tasks** | **585 Total Points** | **4 Difficulty Levels** | **Full API Documentation**

## 🎯 Overview

This project creates a realistic task management system that serves as a training environment for RL agents. It features:

- **24 Programmatic RL Tasks** 🎯 - Spanning 4 difficulty levels (Easy → Very Hard)
- **Beautiful, Modern React UI** - Agents interact with a production-quality interface
- **FastAPI Python Backend** - RESTful API with full CRUD operations
- **SQLite Database** - Realistic mock data for training scenarios
- **Advanced Validation System** - Automated task completion checking with detailed feedback
- **Sophisticated Reward Structure** - 10-50 points per task, 585 points total
- **Full Containerization** - Docker Compose for easy deployment
- **Real-time Dashboard** - Monitor agent performance and environment state

### 🌟 What Makes This Special

- **3x more tasks than typical demos** - 24 vs. standard 8
- **Multi-category challenges** - Workflow, collaboration, quality, optimization
- **Progressive difficulty** - Clear skill progression from beginner to expert
- **Production-ready code** - Type-safe, documented, containerized
- **Complete full-stack** - Frontend, backend, database, validation all included

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Ports 3000 (frontend) and 8000 (backend) available

### Launch the Environment

```bash
# Clone and navigate to the project
cd ex-rl-env

# Start the entire stack
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

That's it! The environment will:
1. Build both frontend and backend containers
2. Initialize the SQLite database
3. Populate with realistic mock data
4. Start the React development server
5. Launch the FastAPI backend

## 🏗️ Architecture

### Backend (`/backend`)

**Tech Stack:** Python 3.11, FastAPI, SQLAlchemy, SQLite

**Key Features:**
- RESTful API with OpenAPI documentation
- Database models with relationships
- CRUD operations for task management
- RL validation system with 8+ predefined tasks
- Reward calculation engine
- Environment state tracking
- Mock data generation with Faker

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

### Frontend (`/frontend`)

**Tech Stack:** React 18, Lucide Icons, Axios

**Key Features:**
- Modern, gradient-based design system
- Responsive layout (mobile-friendly)
- Task board with Kanban-style columns
- Real-time RL dashboard
- Task filtering and search
- Programmatic task validation UI
- Smooth animations and transitions

**Components:**
- `TaskBoard` - Main task management interface
- `TaskCard` - Individual task display with quick actions
- `TaskForm` - Modal for creating new tasks
- `RLDashboard` - RL metrics and validation interface

## 🎓 RL Training Tasks

The environment includes **24 programmatically validated tasks** spanning multiple difficulty levels:

### Easy Tasks (5-20 points)
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
| `perfect_organization` | 35 | All tasks fully organized (assignee, tags, dates) |

### Very Hard Tasks (40-50 points)
| Task | Reward | Description |
|------|--------|-------------|
| `team_collaboration` | 40 | Every member has tasks in all statuses |
| `milestone_achievement` | 40 | Complete 10+ tasks in single episode |
| `clean_slate` | 50 | Archive everything - achieve clean board |

Each task provides:
- ✅ **Programmatic validation** - Automated checking
- 🎯 **Clear success criteria** - Well-defined goals
- 💰 **Reward structure** - Points for completion
- 📊 **Detailed feedback** - Validation results with context

**Task Categories:**
- 📋 Basic Operations (5 tasks) - Foundation skills
- 🎯 Organization & Workflow (10 tasks) - Strategic thinking  
- 🚀 Advanced Goals (6 tasks) - Multi-step reasoning
- 🏆 Expert Challenges (3 tasks) - Sophisticated strategies

**Total Possible Rewards:** 585 points across all tasks

👉 **See [RL_TASKS.md](./RL_TASKS.md) for detailed task documentation**

## 💻 Development

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run locally (without Docker)
uvicorn main:app --reload

# API documentation available at:
# http://localhost:8000/docs
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build
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
CHOKIDAR_USEPOLLING=true
```

## 📊 RL Environment State

The environment exposes comprehensive state information:

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

## 🎨 Design Highlights

- **Modern Gradient Design** - Eye-catching purple gradient theme
- **Glassmorphism Effects** - Subtle backdrop blur and transparency
- **Smooth Animations** - Hover effects and transitions
- **Responsive Layout** - Mobile, tablet, and desktop optimized
- **Accessibility** - Semantic HTML and ARIA labels
- **High Contrast** - Excellent readability and color contrast

## 🔧 Tech Stack Summary

**Containerization:**
- ✅ Docker multi-container setup
- ✅ Docker Compose orchestration
- ✅ Volume mounting for development
- ✅ Environment variable management

**Frontend:**
- ✅ React 18 with Hooks
- ✅ Modern CSS with gradients
- ✅ Component-based architecture
- ✅ Responsive design
- ✅ API integration with Axios

**Backend:**
- ✅ FastAPI framework
- ✅ SQLAlchemy ORM
- ✅ Pydantic models
- ✅ SQLite database
- ✅ CORS middleware
- ✅ OpenAPI documentation

**RL Features:**
- ✅ Programmatic validation
- ✅ Reward calculation
- ✅ State observation
- ✅ Episode management
- ✅ Action tracking
- ✅ Task generation

## 🚀 Production Deployment

For production deployment:

1. **Database**: Switch to PostgreSQL in `database.py`
2. **Environment**: Set production environment variables
3. **Frontend**: Build static files with `npm run build`
4. **Backend**: Use production ASGI server (Gunicorn + Uvicorn)
5. **Reverse Proxy**: Add Nginx for serving static files
6. **HTTPS**: Configure SSL certificates

## 📝 API Documentation

Interactive API documentation is automatically generated:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤖 Agent Integration & Training

### Running the Example Agent

This repository includes a simple example agent that demonstrates autonomous interaction:

```bash
# 1. Ensure environment is running
docker compose up --build

# 2. In a new terminal, set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install requirements
pip install -r agent-requirements.txt

# 4. Run the example agent
python3 example_agent.py
```

The example agent will:
- Connect to the API
- Observe the environment state
- Execute actions (create tasks, update statuses, assign team members)
- Validate RL tasks and collect rewards
- Display a complete episode summary

### Training Real RL Agents

For production RL training with frameworks like:
- **Stable Baselines3** (PPO, DQN, A2C)
- **RLlib** (Ray)
- **Anthropic Computer Use API**
- **OpenAI Gym** integration

See the comprehensive **[AGENT_INTEGRATION.md](./AGENT_INTEGRATION.md)** guide which includes:
- Complete code examples for DQN, PPO
- OpenAI Gym wrapper implementation
- State/action space design
- Reward shaping strategies
- Multi-agent training setup
- Monitoring and evaluation

### Quick Integration Example

```python
import requests

# 1. Observe state
state = requests.get("http://localhost:8000/api/rl/state").json()

# 2. Take action
requests.put("http://localhost:8000/api/tasks/1", 
             json={"status": "completed"})

# 3. Get reward
result = requests.post(
    "http://localhost:8000/api/rl/validate/complete_three_tasks"
).json()

print(f"Reward: {result['reward']}")  # Output: Reward: 15.0
```

## 📈 Metrics and Monitoring

The dashboard provides:
- Total task count
- Actions taken
- Completion rate
- Total rewards earned
- Task distribution by status
- Task distribution by priority
- Episode number
- Real-time validation results

## 🎯 Future Enhancements

- [ ] Add more complex multi-step tasks
- [ ] Implement user authentication
- [ ] Add task dependencies and subtasks
- [ ] WebSocket support for real-time updates
- [ ] Export/import task data
- [ ] Advanced filtering and search
- [ ] Task history and audit log
- [ ] Custom reward functions
- [ ] Multi-agent training support

## 📄 License

MIT License - Feel free to use this for training and development!

---

**Built with ❤️ as a demonstration of full-stack RL environment development skills.**

