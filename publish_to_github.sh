#!/bin/bash
# Quick publish script for GitHub

echo "🚀 Publishing RL Environment to GitHub"
echo "======================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo ""
fi

# Add all files (respecting .gitignore)
echo "📝 Staging files..."
git add .
echo ""

# Show what will be committed
echo "📋 Files to be committed:"
git status --short
echo ""

# Create commit
echo "💾 Creating commit..."
git commit -m "feat: Complete RL training environment with 24 tasks

Production-ready RL training environment for computer-use agents

Features:
- 24 programmatic RL tasks across 4 difficulty levels
- Full-stack: React frontend + FastAPI backend
- Docker containerization for one-command deployment
- Example agent with autonomous training capability
- Comprehensive documentation (5 guides, 2,300+ lines)
- Beautiful responsive UI with task board and RL dashboard
- Complete API with OpenAPI documentation

Technical Stack:
- Frontend: React 18, Lucide Icons, Axios
- Backend: FastAPI, SQLAlchemy, Pydantic
- Database: SQLite with realistic mock data
- Deployment: Docker Compose
- Code Quality: Type hints, clean architecture, 3,846 LOC

RL Features:
- State observation via REST API
- Action execution through CRUD operations
- Reward validation with programmatic checks
- Episode management and reset capability
- 585 total reward points across progressive difficulty"

echo ""
echo "✅ Repository ready!"
echo ""
echo "📤 Next steps:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "2. Repository name: rl-task-environment (or your choice)"
echo "3. Make it PUBLIC"
echo "4. Do NOT initialize with README"
echo "5. Copy your repository URL"
echo "6. Run these commands:"
echo ""
echo "   git remote add origin YOUR_GITHUB_URL"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "🏷️  Suggested GitHub topics:"
echo "   reinforcement-learning, machine-learning, fastapi, react,"
echo "   docker, python, full-stack, computer-use-agents, openai-gym"
echo ""
