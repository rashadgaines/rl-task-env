# Setup Guide

Complete setup instructions for the Task Management RL Environment.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

Check your installation:
```bash
docker --version
docker-compose --version
```

Installation links:
- Mac: [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- Windows: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- Linux: [Docker installation guide](https://docs.docker.com/engine/install/)

## Quick Start

### 1. Launch Application

```bash
docker compose up --build
```

This will:
- Build both frontend and backend containers
- Initialize the SQLite database
- Populate with mock data
- Start both services

### 2. Access

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 3. Stop

Press `Ctrl+C`, then:
```bash
docker compose down
```

## Development Setup

Run services individually for development:

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Available at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm start
```

Available at http://localhost:3000

Note: Backend must be running first.

## Troubleshooting

### Port Already in Use

Mac/Linux:
```bash
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

Windows:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Or modify ports in `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"
  frontend:
    ports:
      - "3001:3000"
```

### Docker Build Fails

Clear cache and rebuild:
```bash
docker compose down
docker system prune -a
docker compose up --build
```

Ensure Docker has at least 4GB memory allocated.

### Database Not Initializing

Remove volume and rebuild:
```bash
docker compose down -v
docker compose up --build
```

Check logs:
```bash
docker compose logs backend
```

### Frontend Can't Connect

Verify backend is running:
```bash
curl http://localhost:8000
```

Check CORS configuration allows `http://localhost:3000`.

Verify `API_URL` in `frontend/src/services/api.js`.

### Permission Issues (Linux)

```bash
sudo chown -R $USER:$USER .
chmod -R 755 .
```

## Verification

### Backend Health

```bash
curl http://localhost:8000
```

Expected response:
```json
{
  "message": "Task Management RL Environment API",
  "version": "1.0.0",
  "status": "operational"
}
```

### API Endpoints

```bash
curl http://localhost:8000/api/tasks     # All tasks
curl http://localhost:8000/api/rl/state  # RL state
```

### Frontend

Open http://localhost:3000 and verify:
- Tasks display in board
- RL Dashboard tab works
- Task creation functions
- Filters operate correctly

### RL Validation

In RL Dashboard:
1. Select an RL task
2. Click "Validate"
3. Verify results and rewards display

## Environment Variables

### Backend (`backend/.env`)

```env
DATABASE_URL=sqlite:////data/tasks.db
LOG_LEVEL=info
```

### Frontend (`frontend/.env`)

```env
REACT_APP_API_URL=http://localhost:8000
```

## Useful Commands

```bash
# Background mode
docker compose up -d

# View logs
docker compose logs -f

# Restart service
docker compose restart backend

# Rebuild service
docker compose up --build backend

# Remove all
docker compose down -v

# Execute in container
docker compose exec backend bash
docker compose exec frontend sh
```

## Development Tips

- Both services support hot reload
- Reset environment via RL Dashboard button
- Test API at http://localhost:8000/docs
- Customize mock data in `backend/mock_data.py`
- Add RL tasks in `backend/rl_validator.py`
