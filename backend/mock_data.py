from sqlalchemy.orm import Session
from database import Task
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker()


def populate_mock_data(db: Session):
    """Populate database with realistic mock data"""
    
    # Check if data already exists
    existing_tasks = db.query(Task).count()
    if existing_tasks > 0:
        return
    
    # Team members
    team_members = [
        "Alice Chen",
        "Bob Smith",
        "Carol Williams",
        "David Brown",
        "Emma Davis",
        None  # Some unassigned
    ]
    
    # Common tags for realistic categorization
    tag_categories = {
        "type": ["bug", "feature", "refactor", "documentation", "testing"],
        "area": ["frontend", "backend", "database", "api", "ui"],
        "sprint": ["sprint-1", "sprint-2", "sprint-3"],
        "effort": ["quick-win", "complex", "research"],
    }
    
    # Predefined realistic tasks
    task_templates = [
        {
            "title": "Fix login authentication bug",
            "description": "Users are experiencing intermittent login failures. Investigate and fix the authentication flow.",
            "priority": "urgent",
            "status": "in_progress",
            "tags": ["bug", "backend", "api", "sprint-2"]
        },
        {
            "title": "Implement dark mode toggle",
            "description": "Add a dark mode toggle to the settings page with persistent user preference.",
            "priority": "high",
            "status": "todo",
            "tags": ["feature", "frontend", "ui", "sprint-2"]
        },
        {
            "title": "Optimize database queries",
            "description": "Several API endpoints are slow. Profile and optimize N+1 query issues.",
            "priority": "high",
            "status": "todo",
            "tags": ["refactor", "database", "backend", "complex"]
        },
        {
            "title": "Write API documentation",
            "description": "Document all REST API endpoints with request/response examples.",
            "priority": "medium",
            "status": "completed",
            "tags": ["documentation", "api", "sprint-1"]
        },
        {
            "title": "Add unit tests for user service",
            "description": "Increase test coverage for the user service module to at least 80%.",
            "priority": "medium",
            "status": "todo",
            "tags": ["testing", "backend", "sprint-2"]
        },
        {
            "title": "Design new landing page",
            "description": "Create mockups for the new landing page with improved conversion rate.",
            "priority": "low",
            "status": "completed",
            "tags": ["feature", "frontend", "ui", "sprint-1"]
        },
        {
            "title": "Set up CI/CD pipeline",
            "description": "Configure GitHub Actions for automated testing and deployment.",
            "priority": "high",
            "status": "in_progress",
            "tags": ["refactor", "backend", "sprint-2", "complex"]
        },
        {
            "title": "Investigate performance regression",
            "description": "Page load times have increased by 30% since last deployment. Find and fix the cause.",
            "priority": "urgent",
            "status": "todo",
            "tags": ["bug", "frontend", "research"]
        },
        {
            "title": "Update dependencies",
            "description": "Update all npm packages to latest stable versions and test for breaking changes.",
            "priority": "low",
            "status": "todo",
            "tags": ["refactor", "frontend", "backend", "quick-win"]
        },
        {
            "title": "Add email notifications",
            "description": "Send email notifications when tasks are assigned or updated.",
            "priority": "medium",
            "status": "todo",
            "tags": ["feature", "backend", "api", "sprint-3"]
        },
        {
            "title": "Refactor authentication module",
            "description": "Clean up authentication code and improve error handling.",
            "priority": "low",
            "status": "completed",
            "tags": ["refactor", "backend", "api", "sprint-1"]
        },
        {
            "title": "Add task filtering by date",
            "description": "Allow users to filter tasks by creation date and due date ranges.",
            "priority": "medium",
            "status": "todo",
            "tags": ["feature", "frontend", "ui", "sprint-3"]
        },
        {
            "title": "Fix mobile responsive issues",
            "description": "Several UI components break on mobile devices. Fix responsive layouts.",
            "priority": "high",
            "status": "in_progress",
            "tags": ["bug", "frontend", "ui", "sprint-2"]
        },
        {
            "title": "Implement task search",
            "description": "Add full-text search functionality for tasks with highlighting.",
            "priority": "medium",
            "status": "todo",
            "tags": ["feature", "backend", "database", "sprint-3"]
        },
        {
            "title": "Create onboarding tutorial",
            "description": "Build an interactive tutorial for new users to learn the platform.",
            "priority": "low",
            "status": "todo",
            "tags": ["feature", "frontend", "ui", "documentation"]
        },
    ]
    
    # Create tasks
    for i, template in enumerate(task_templates):
        # Assign team member
        assigned_to = random.choice(team_members)
        
        # Calculate due date based on priority
        days_offset = {
            "urgent": 1,
            "high": 5,
            "medium": 14,
            "low": 30
        }
        
        due_offset = days_offset.get(template["priority"], 14)
        # Make some tasks overdue
        if random.random() < 0.2:
            due_date = datetime.utcnow() - timedelta(days=random.randint(1, 5))
        else:
            due_date = datetime.utcnow() + timedelta(days=random.randint(1, due_offset))
        
        task = Task(
            title=template["title"],
            description=template["description"],
            status=template["status"],
            priority=template["priority"],
            tags=template["tags"],
            assigned_to=assigned_to,
            due_date=due_date,
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            updated_at=datetime.utcnow() - timedelta(days=random.randint(0, 5))
        )
        
        db.add(task)
    
    db.commit()
    print(f"✅ Created {len(task_templates)} realistic tasks with mock data")

