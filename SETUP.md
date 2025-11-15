# Setup Guide

This guide will help you get the Task Management RL Environment up and running in minutes.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)

### Check Your Installation

```bash
docker --version
docker-compose --version
```

If you need to install Docker:
- **Mac**: Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- **Windows**: Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- **Linux**: Follow the [official Docker installation guide](https://docs.docker.com/engine/install/)

## Quick Start (Recommended)

### 1. Navigate to the Project Directory

```bash
cd /Users/rashadgaines/ex-rl-env
```

### 2. Launch the Application

```bash
docker-compose up --build
```

This command will:
- Build the backend Docker container
- Build the frontend Docker container
- Create a data volume for the database
- Initialize the SQLite database
- Populate with realistic mock data
- Start both services

### 3. Access the Application

Once you see the startup messages, open your browser:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Stop the Application

Press `Ctrl+C` in the terminal, then run:

```bash
docker-compose down
```

## Development Setup

If you want to run the services individually for development:

### Backend Only

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create data directory
mkdir -p ../data

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000

### Frontend Only

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at http://localhost:3000

**Note**: Make sure the backend is running first, as the frontend depends on it.

## Troubleshooting

### Port Already in Use

If you see an error about ports 3000 or 8000 being in use:

```bash
# Find and kill the process using port 8000 (Mac/Linux)
lsof -ti:8000 | xargs kill -9

# Find and kill the process using port 3000 (Mac/Linux)
lsof -ti:3000 | xargs kill -9

# On Windows, use:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Alternatively, modify the ports in `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Changed from 8000:8000
  
  frontend:
    ports:
      - "3001:3000"  # Changed from 3000:3000
```

### Docker Build Fails

If the Docker build fails:

1. **Clear Docker cache**:
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

2. **Check Docker resources**: Ensure Docker has enough memory allocated (at least 4GB recommended)

### Database Not Initializing

If the database doesn't populate:

1. **Remove the data volume**:
```bash
docker-compose down -v
docker-compose up --build
```

2. **Check logs**:
```bash
docker-compose logs backend
```

### Frontend Can't Connect to Backend

1. **Check backend is running**:
```bash
curl http://localhost:8000
```

2. **Verify CORS configuration**: The backend should allow requests from `http://localhost:3000`

3. **Check environment variables**: In `frontend/src/services/api.js`, verify `API_URL` is correct

### Permission Issues (Linux)

If you encounter permission issues on Linux:

```bash
sudo chown -R $USER:$USER .
chmod -R 755 .
```

## Testing the Environment

### 1. Check Backend Health

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

### 2. Test API Endpoints

Get all tasks:
```bash
curl http://localhost:8000/api/tasks
```

Get RL state:
```bash
curl http://localhost:8000/api/rl/state
```

### 3. Test Frontend

Open http://localhost:3000 and verify:
- Tasks are displayed in the board
- You can switch to the RL Dashboard tab
- You can create new tasks
- Filters work correctly

### 4. Test RL Validation

In the RL Dashboard:
1. Click on any RL task
2. Click "Validate"
3. Check if validation results appear
4. Verify rewards are calculated

## Environment Variables

### Backend

Create `backend/.env` (optional):

```env
DATABASE_URL=sqlite:////data/tasks.db
LOG_LEVEL=info
```

### Frontend

Create `frontend/.env` (optional):

```env
REACT_APP_API_URL=http://localhost:8000
```

## Production Deployment

For production deployment:

### 1. Update Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/tasks
    command: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### 2. Build Frontend for Production

```bash
cd frontend
npm run build
```

### 3. Use Production Server for Backend

Update `backend/Dockerfile`:

```dockerfile
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## Next Steps

1. **Explore the UI**: Navigate through the task board and RL dashboard
2. **Test RL Tasks**: Try completing the validation tasks
3. **Read the API Docs**: Visit http://localhost:8000/docs
4. **Customize**: Modify the code to add new features
5. **Integrate Agent**: Connect your RL agent to the API endpoints

## Getting Help

If you encounter any issues:

1. Check the **Troubleshooting** section above
2. Review the logs: `docker-compose logs`
3. Consult the **README.md** for more details
4. Check Docker and Docker Compose documentation

## Useful Commands

```bash
# Start in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Restart a specific service
docker-compose restart backend

# Rebuild a specific service
docker-compose up --build backend

# Remove all containers and volumes
docker-compose down -v

# Execute commands in running container
docker-compose exec backend bash
docker-compose exec frontend sh
```

## Development Tips

1. **Hot Reload**: Both frontend and backend support hot reload in development mode
2. **Database Reset**: Use the "Reset Environment" button in the RL Dashboard
3. **API Testing**: Use the Swagger UI at http://localhost:8000/docs
4. **Mock Data**: Modify `backend/mock_data.py` to customize initial data
5. **New RL Tasks**: Add validation functions in `backend/rl_validator.py`

---

**You're all set!** 🚀 Enjoy exploring the RL training environment!

