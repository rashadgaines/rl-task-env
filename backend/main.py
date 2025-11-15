from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import get_db, init_db, Task
from models import TaskCreate, TaskUpdate, TaskResponse, ValidationResult, RLEnvironmentState
from rl_validator import RLValidator
from mock_data import populate_mock_data

app = FastAPI(title="Task Management RL Environment", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RL Validator
rl_validator = RLValidator()


@app.on_event("startup")
async def startup_event():
    """Initialize database and populate with mock data"""
    init_db()
    db = next(get_db())
    populate_mock_data(db)
    print("✅ Database initialized with mock data")


@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Task Management RL Environment API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all tasks with optional filtering"""
    from crud import get_tasks as get_tasks_crud
    tasks = get_tasks_crud(db, status=status, priority=priority)
    return tasks


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    from crud import get_task
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    from crud import create_task as create_task_crud
    new_task = create_task_crud(db, task)
    
    # Track action for RL validation
    rl_validator.track_action("create_task", {
        "task_id": new_task.id,
        "title": new_task.title,
        "priority": new_task.priority
    })
    
    return new_task


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task"""
    from crud import update_task as update_task_crud
    updated_task = update_task_crud(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Track action for RL validation
    rl_validator.track_action("update_task", {
        "task_id": task_id,
        "updates": task.dict(exclude_unset=True)
    })
    
    return updated_task


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    from crud import delete_task as delete_task_crud
    success = delete_task_crud(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Track action for RL validation
    rl_validator.track_action("delete_task", {"task_id": task_id})
    
    return {"message": "Task deleted successfully"}


@app.post("/api/rl/reset")
async def reset_environment(db: Session = Depends(get_db)):
    """Reset the RL environment to initial state"""
    from crud import reset_database
    reset_database(db)
    populate_mock_data(db)
    rl_validator.reset()
    return {"message": "Environment reset successfully"}


@app.get("/api/rl/state", response_model=RLEnvironmentState)
async def get_rl_state(db: Session = Depends(get_db)):
    """Get current RL environment state"""
    from crud import get_tasks as get_tasks_crud
    tasks = get_tasks_crud(db)
    
    state = rl_validator.get_state(tasks)
    return state


@app.post("/api/rl/validate/{task_name}", response_model=ValidationResult)
async def validate_task(task_name: str, db: Session = Depends(get_db)):
    """Validate if a specific RL task has been completed"""
    from crud import get_tasks as get_tasks_crud
    tasks = get_tasks_crud(db)
    
    result = rl_validator.validate_task(task_name, tasks)
    return result


@app.get("/api/rl/tasks")
async def get_available_rl_tasks():
    """Get all available RL tasks that agents can attempt"""
    return rl_validator.get_available_tasks()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

