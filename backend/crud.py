from sqlalchemy.orm import Session
from database import Task
from models import TaskCreate, TaskUpdate
from typing import List, Optional
from datetime import datetime


def get_tasks(db: Session, status: Optional[str] = None, priority: Optional[str] = None) -> List[Task]:
    """Get all tasks with optional filtering"""
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    
    return query.all()


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Get a single task by ID"""
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate) -> Task:
    """Create a new task"""
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        tags=task.tags or [],
        assigned_to=task.assigned_to,
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate) -> Optional[Task]:
    """Update an existing task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        return None
    
    update_data = task.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True


def reset_database(db: Session):
    """Reset the database by deleting all tasks"""
    db.query(Task).delete()
    db.commit()

