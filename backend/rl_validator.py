from typing import List, Dict, Any, Callable
from models import ValidationResult, RLEnvironmentState
from database import Task
from datetime import datetime, timedelta


class RLTask:
    """Represents an RL task that an agent can attempt to complete"""
    
    def __init__(
        self,
        name: str,
        description: str,
        validation_fn: Callable,
        reward: float,
        difficulty: str
    ):
        self.name = name
        self.description = description
        self.validation_fn = validation_fn
        self.reward = reward
        self.difficulty = difficulty


class RLValidator:
    """
    Validates agent actions and calculates rewards for RL training.
    Tracks environment state and provides programmatic task validation.
    """
    
    def __init__(self):
        self.actions_taken = 0
        self.current_reward = 0.0
        self.episode_number = 1
        self.action_history = []
        self.rl_tasks = self._define_rl_tasks()
    
    def _define_rl_tasks(self) -> Dict[str, RLTask]:
        """Define all available RL tasks with validation logic"""
        return {
            "create_urgent_task": RLTask(
                name="create_urgent_task",
                description="Create a new task with 'urgent' priority",
                validation_fn=self._validate_create_urgent_task,
                reward=10.0,
                difficulty="easy"
            ),
            "complete_three_tasks": RLTask(
                name="complete_three_tasks",
                description="Mark at least 3 tasks as completed",
                validation_fn=self._validate_complete_three_tasks,
                reward=15.0,
                difficulty="easy"
            ),
            "organize_by_priority": RLTask(
                name="organize_by_priority",
                description="Ensure all high priority tasks are either in_progress or completed",
                validation_fn=self._validate_organize_by_priority,
                reward=20.0,
                difficulty="medium"
            ),
            "clear_overdue_tasks": RLTask(
                name="clear_overdue_tasks",
                description="Complete or delete all tasks with past due dates",
                validation_fn=self._validate_clear_overdue_tasks,
                reward=25.0,
                difficulty="medium"
            ),
            "assign_all_tasks": RLTask(
                name="assign_all_tasks",
                description="Assign all unassigned tasks to team members",
                validation_fn=self._validate_assign_all_tasks,
                reward=15.0,
                difficulty="easy"
            ),
            "achieve_80_completion": RLTask(
                name="achieve_80_completion",
                description="Achieve at least 80% task completion rate",
                validation_fn=self._validate_achievement_80_completion,
                reward=30.0,
                difficulty="hard"
            ),
            "organize_with_tags": RLTask(
                name="organize_with_tags",
                description="Add at least 2 tags to every task for better organization",
                validation_fn=self._validate_organize_with_tags,
                reward=20.0,
                difficulty="medium"
            ),
            "archive_completed": RLTask(
                name="archive_completed",
                description="Archive all completed tasks to clean up the board",
                validation_fn=self._validate_archive_completed,
                reward=15.0,
                difficulty="easy"
            ),
            "balance_workload": RLTask(
                name="balance_workload",
                description="Distribute tasks evenly across all team members (max difference of 2 tasks)",
                validation_fn=self._validate_balance_workload,
                reward=25.0,
                difficulty="medium"
            ),
            "prioritize_urgent_items": RLTask(
                name="prioritize_urgent_items",
                description="Ensure all urgent tasks are in_progress and have near due dates",
                validation_fn=self._validate_prioritize_urgent_items,
                reward=20.0,
                difficulty="medium"
            ),
            "create_sprint_backlog": RLTask(
                name="create_sprint_backlog",
                description="Create at least 5 new tasks with 'sprint' tags and assign them",
                validation_fn=self._validate_create_sprint_backlog,
                reward=30.0,
                difficulty="hard"
            ),
            "eliminate_technical_debt": RLTask(
                name="eliminate_technical_debt",
                description="Complete or archive all tasks tagged with 'refactor' or 'technical-debt'",
                validation_fn=self._validate_eliminate_technical_debt,
                reward=25.0,
                difficulty="medium"
            ),
            "achieve_zero_bugs": RLTask(
                name="achieve_zero_bugs",
                description="Complete or delete all tasks tagged with 'bug'",
                validation_fn=self._validate_achieve_zero_bugs,
                reward=35.0,
                difficulty="hard"
            ),
            "optimize_task_flow": RLTask(
                name="optimize_task_flow",
                description="Ensure todo < in_progress < completed (pipeline optimization)",
                validation_fn=self._validate_optimize_task_flow,
                reward=30.0,
                difficulty="hard"
            ),
            "team_collaboration": RLTask(
                name="team_collaboration",
                description="Ensure every team member has at least one task in each status category",
                validation_fn=self._validate_team_collaboration,
                reward=40.0,
                difficulty="very_hard"
            ),
            "deadline_management": RLTask(
                name="deadline_management",
                description="Ensure all tasks due within 3 days are in_progress or completed",
                validation_fn=self._validate_deadline_management,
                reward=25.0,
                difficulty="medium"
            ),
            "quality_assurance": RLTask(
                name="quality_assurance",
                description="Add 'tested' or 'reviewed' tags to all completed tasks",
                validation_fn=self._validate_quality_assurance,
                reward=20.0,
                difficulty="medium"
            ),
            "perfect_organization": RLTask(
                name="perfect_organization",
                description="All tasks must have: assignee, 2+ tags, and due date",
                validation_fn=self._validate_perfect_organization,
                reward=35.0,
                difficulty="hard"
            ),
            "reduce_wip": RLTask(
                name="reduce_wip",
                description="Reduce work-in-progress to maximum 5 tasks",
                validation_fn=self._validate_reduce_wip,
                reward=20.0,
                difficulty="medium"
            ),
            "feature_completion": RLTask(
                name="feature_completion",
                description="Complete all tasks tagged with 'feature'",
                validation_fn=self._validate_feature_completion,
                reward=30.0,
                difficulty="hard"
            ),
            "clean_slate": RLTask(
                name="clean_slate",
                description="Archive or complete all tasks - only archived tasks should remain",
                validation_fn=self._validate_clean_slate,
                reward=50.0,
                difficulty="very_hard"
            ),
            "milestone_achievement": RLTask(
                name="milestone_achievement",
                description="Complete at least 10 tasks in a single episode",
                validation_fn=self._validate_milestone_achievement,
                reward=40.0,
                difficulty="very_hard"
            ),
            "documentation_complete": RLTask(
                name="documentation_complete",
                description="All tasks tagged 'documentation' must be completed",
                validation_fn=self._validate_documentation_complete,
                reward=20.0,
                difficulty="easy"
            ),
            "no_low_priority_in_progress": RLTask(
                name="no_low_priority_in_progress",
                description="Ensure no low priority tasks are in_progress when high priority tasks exist",
                validation_fn=self._validate_no_low_priority_in_progress,
                reward=25.0,
                difficulty="medium"
            ),
        }
    
    def track_action(self, action_type: str, action_data: Dict[str, Any]):
        """Track an action taken by the agent"""
        self.actions_taken += 1
        self.action_history.append({
            "type": action_type,
            "data": action_data,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_state(self, tasks: List[Task]) -> RLEnvironmentState:
        """Get current environment state for RL observations"""
        tasks_by_status = {}
        tasks_by_priority = {}
        
        for task in tasks:
            tasks_by_status[task.status] = tasks_by_status.get(task.status, 0) + 1
            tasks_by_priority[task.priority] = tasks_by_priority.get(task.priority, 0) + 1
        
        completed = tasks_by_status.get("completed", 0)
        total = len(tasks)
        completion_rate = (completed / total * 100) if total > 0 else 0.0
        
        return RLEnvironmentState(
            total_tasks=total,
            tasks_by_status=tasks_by_status,
            tasks_by_priority=tasks_by_priority,
            completion_rate=completion_rate,
            actions_taken=self.actions_taken,
            current_reward=self.current_reward,
            episode_number=self.episode_number
        )
    
    def validate_task(self, task_name: str, tasks: List[Task]) -> ValidationResult:
        """Validate if a specific RL task has been completed"""
        if task_name not in self.rl_tasks:
            return ValidationResult(
                task_name=task_name,
                completed=False,
                reward=0.0,
                feedback=f"Unknown task: {task_name}",
                details={}
            )
        
        rl_task = self.rl_tasks[task_name]
        result = rl_task.validation_fn(tasks)
        
        if result["completed"]:
            self.current_reward += rl_task.reward
        
        return ValidationResult(
            task_name=task_name,
            completed=result["completed"],
            reward=rl_task.reward if result["completed"] else 0.0,
            feedback=result["feedback"],
            details=result.get("details", {})
        )
    
    def get_available_tasks(self) -> List[Dict[str, Any]]:
        """Get list of all available RL tasks"""
        return [
            {
                "name": task.name,
                "description": task.description,
                "reward": task.reward,
                "difficulty": task.difficulty
            }
            for task in self.rl_tasks.values()
        ]
    
    def reset(self):
        """Reset the validator state for a new episode"""
        self.actions_taken = 0
        self.current_reward = 0.0
        self.episode_number += 1
        self.action_history = []
    
    # Validation functions for each RL task
    
    def _validate_create_urgent_task(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if an urgent task exists"""
        urgent_tasks = [t for t in tasks if t.priority == "urgent"]
        completed = len(urgent_tasks) > 0
        
        return {
            "completed": completed,
            "feedback": f"✅ Found {len(urgent_tasks)} urgent task(s)" if completed else "❌ No urgent tasks found. Create a task with 'urgent' priority.",
            "details": {"urgent_task_count": len(urgent_tasks)}
        }
    
    def _validate_complete_three_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if at least 3 tasks are completed"""
        completed_tasks = [t for t in tasks if t.status == "completed"]
        count = len(completed_tasks)
        completed = count >= 3
        
        return {
            "completed": completed,
            "feedback": f"✅ {count} tasks completed (target: 3)" if completed else f"❌ Only {count} tasks completed. Need 3 or more.",
            "details": {"completed_count": count, "target": 3}
        }
    
    def _validate_organize_by_priority(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if all high priority tasks are in progress or completed"""
        high_priority = [t for t in tasks if t.priority == "high"]
        organized = [t for t in high_priority if t.status in ["in_progress", "completed"]]
        
        completed = len(high_priority) > 0 and len(organized) == len(high_priority)
        
        return {
            "completed": completed,
            "feedback": f"✅ All {len(high_priority)} high priority tasks are organized" if completed else f"❌ {len(high_priority) - len(organized)} high priority tasks still in 'todo' state",
            "details": {"high_priority_count": len(high_priority), "organized_count": len(organized)}
        }
    
    def _validate_clear_overdue_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if all overdue tasks are completed or deleted"""
        now = datetime.utcnow()
        overdue_tasks = [
            t for t in tasks 
            if t.due_date and t.due_date < now and t.status not in ["completed", "archived"]
        ]
        
        completed = len(overdue_tasks) == 0
        
        return {
            "completed": completed,
            "feedback": "✅ No overdue tasks remaining" if completed else f"❌ {len(overdue_tasks)} overdue task(s) need attention",
            "details": {"overdue_count": len(overdue_tasks)}
        }
    
    def _validate_assign_all_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if all tasks are assigned"""
        unassigned = [t for t in tasks if not t.assigned_to]
        completed = len(unassigned) == 0 and len(tasks) > 0
        
        return {
            "completed": completed,
            "feedback": "✅ All tasks are assigned" if completed else f"❌ {len(unassigned)} task(s) need assignment",
            "details": {"unassigned_count": len(unassigned), "total_tasks": len(tasks)}
        }
    
    def _validate_achievement_80_completion(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if completion rate is at least 80%"""
        if len(tasks) == 0:
            return {
                "completed": False,
                "feedback": "❌ No tasks exist",
                "details": {"completion_rate": 0.0}
            }
        
        completed_tasks = [t for t in tasks if t.status == "completed"]
        completion_rate = (len(completed_tasks) / len(tasks)) * 100
        completed = completion_rate >= 80.0
        
        return {
            "completed": completed,
            "feedback": f"✅ Completion rate: {completion_rate:.1f}%" if completed else f"❌ Completion rate: {completion_rate:.1f}% (target: 80%)",
            "details": {"completion_rate": completion_rate, "completed_count": len(completed_tasks), "total_count": len(tasks)}
        }
    
    def _validate_organize_with_tags(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if all tasks have at least 2 tags"""
        tasks_with_enough_tags = [t for t in tasks if t.tags and len(t.tags) >= 2]
        completed = len(tasks) > 0 and len(tasks_with_enough_tags) == len(tasks)
        
        return {
            "completed": completed,
            "feedback": "✅ All tasks have 2+ tags" if completed else f"❌ {len(tasks) - len(tasks_with_enough_tags)} task(s) need more tags",
            "details": {"tasks_with_tags": len(tasks_with_enough_tags), "total_tasks": len(tasks)}
        }
    
    def _validate_archive_completed(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if all completed tasks are archived"""
        completed_not_archived = [t for t in tasks if t.status == "completed"]
        completed = len(completed_not_archived) == 0
        
        return {
            "completed": completed,
            "feedback": "✅ All completed tasks are archived" if completed else f"❌ {len(completed_not_archived)} completed task(s) need archiving",
            "details": {"completed_not_archived": len(completed_not_archived)}
        }
    
    def _validate_balance_workload(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if workload is balanced across team members"""
        assigned_tasks = [t for t in tasks if t.assigned_to and t.status != "archived"]
        
        if len(assigned_tasks) == 0:
            return {
                "completed": False,
                "feedback": "❌ No assigned tasks found",
                "details": {}
            }
        
        # Count tasks per person
        workload = {}
        for task in assigned_tasks:
            workload[task.assigned_to] = workload.get(task.assigned_to, 0) + 1
        
        if len(workload) < 2:
            return {
                "completed": False,
                "feedback": "❌ Need at least 2 team members with tasks",
                "details": {"team_members": len(workload)}
            }
        
        counts = list(workload.values())
        max_diff = max(counts) - min(counts)
        completed = max_diff <= 2
        
        return {
            "completed": completed,
            "feedback": f"✅ Workload balanced (max difference: {max_diff})" if completed else f"❌ Workload imbalanced (difference: {max_diff}, max allowed: 2)",
            "details": {"workload": workload, "max_difference": max_diff}
        }
    
    def _validate_prioritize_urgent_items(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if all urgent tasks are in progress"""
        urgent_tasks = [t for t in tasks if t.priority == "urgent"]
        
        if len(urgent_tasks) == 0:
            return {
                "completed": True,
                "feedback": "✅ No urgent tasks (or create some to complete this task)",
                "details": {"urgent_count": 0}
            }
        
        urgent_in_progress = [t for t in urgent_tasks if t.status == "in_progress"]
        completed = len(urgent_in_progress) == len(urgent_tasks)
        
        return {
            "completed": completed,
            "feedback": f"✅ All {len(urgent_tasks)} urgent tasks are in progress" if completed else f"❌ {len(urgent_tasks) - len(urgent_in_progress)} urgent task(s) not in progress",
            "details": {"urgent_total": len(urgent_tasks), "urgent_in_progress": len(urgent_in_progress)}
        }
    
    def _validate_create_sprint_backlog(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if sprint backlog has been created"""
        sprint_tasks = [
            t for t in tasks 
            if t.tags and any('sprint' in tag.lower() for tag in t.tags) and t.assigned_to
        ]
        
        completed = len(sprint_tasks) >= 5
        
        return {
            "completed": completed,
            "feedback": f"✅ Sprint backlog created with {len(sprint_tasks)} tasks" if completed else f"❌ Only {len(sprint_tasks)} sprint tasks created (need 5+)",
            "details": {"sprint_task_count": len(sprint_tasks), "target": 5}
        }
    
    def _validate_eliminate_technical_debt(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if all technical debt tasks are resolved"""
        debt_tasks = [
            t for t in tasks 
            if t.tags and any(tag.lower() in ['refactor', 'technical-debt', 'debt'] for tag in t.tags)
            and t.status not in ["completed", "archived"]
        ]
        
        completed = len(debt_tasks) == 0
        
        return {
            "completed": completed,
            "feedback": "✅ All technical debt eliminated" if completed else f"❌ {len(debt_tasks)} technical debt task(s) remaining",
            "details": {"debt_tasks_remaining": len(debt_tasks)}
        }
    
    def _validate_achieve_zero_bugs(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate if all bug tasks are resolved"""
        bug_tasks = [
            t for t in tasks 
            if t.tags and 'bug' in [tag.lower() for tag in t.tags]
            and t.status not in ["completed", "archived"]
        ]
        
        completed = len(bug_tasks) == 0
        
        return {
            "completed": completed,
            "feedback": "✅ Zero bugs! All bug tasks resolved" if completed else f"❌ {len(bug_tasks)} bug(s) still open",
            "details": {"bugs_remaining": len(bug_tasks)}
        }
    
    def _validate_optimize_task_flow(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate optimal task flow (todo < in_progress < completed)"""
        todo_count = len([t for t in tasks if t.status == "todo"])
        in_progress_count = len([t for t in tasks if t.status == "in_progress"])
        completed_count = len([t for t in tasks if t.status == "completed"])
        
        # Optimal flow: fewer tasks in early stages, more in later stages
        completed = todo_count < in_progress_count < completed_count
        
        return {
            "completed": completed,
            "feedback": f"✅ Optimal flow: todo({todo_count}) < in_progress({in_progress_count}) < completed({completed_count})" if completed else f"❌ Flow needs optimization: todo({todo_count}), in_progress({in_progress_count}), completed({completed_count})",
            "details": {
                "todo": todo_count,
                "in_progress": in_progress_count,
                "completed": completed_count
            }
        }
    
    def _validate_team_collaboration(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that every team member has tasks in all status categories"""
        assigned_tasks = [t for t in tasks if t.assigned_to]
        
        # Get unique team members
        team_members = set(t.assigned_to for t in assigned_tasks)
        
        if len(team_members) < 2:
            return {
                "completed": False,
                "feedback": "❌ Need at least 2 team members with tasks",
                "details": {}
            }
        
        # Check if each member has tasks in todo, in_progress, and completed
        collaboration_score = {}
        for member in team_members:
            member_tasks = [t for t in assigned_tasks if t.assigned_to == member]
            statuses = set(t.status for t in member_tasks)
            has_all = {"todo", "in_progress", "completed"}.issubset(statuses)
            collaboration_score[member] = has_all
        
        completed = all(collaboration_score.values())
        
        return {
            "completed": completed,
            "feedback": "✅ Full team collaboration achieved" if completed else f"❌ {sum(not v for v in collaboration_score.values())} team member(s) need tasks in all statuses",
            "details": {"collaboration_score": collaboration_score}
        }
    
    def _validate_deadline_management(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that tasks due soon are being worked on"""
        now = datetime.utcnow()
        three_days = timedelta(days=3)
        
        upcoming_tasks = [
            t for t in tasks 
            if t.due_date and now <= t.due_date <= now + three_days
        ]
        
        if len(upcoming_tasks) == 0:
            return {
                "completed": True,
                "feedback": "✅ No upcoming deadlines",
                "details": {"upcoming_count": 0}
            }
        
        managed_tasks = [
            t for t in upcoming_tasks 
            if t.status in ["in_progress", "completed"]
        ]
        
        completed = len(managed_tasks) == len(upcoming_tasks)
        
        return {
            "completed": completed,
            "feedback": f"✅ All {len(upcoming_tasks)} upcoming deadlines are managed" if completed else f"❌ {len(upcoming_tasks) - len(managed_tasks)} upcoming task(s) not in progress",
            "details": {"upcoming_total": len(upcoming_tasks), "managed": len(managed_tasks)}
        }
    
    def _validate_quality_assurance(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that completed tasks have QA tags"""
        completed_tasks = [t for t in tasks if t.status == "completed"]
        
        if len(completed_tasks) == 0:
            return {
                "completed": False,
                "feedback": "❌ No completed tasks to validate",
                "details": {}
            }
        
        qa_tasks = [
            t for t in completed_tasks
            if t.tags and any(tag.lower() in ['tested', 'reviewed', 'qa', 'approved'] for tag in t.tags)
        ]
        
        completed = len(qa_tasks) == len(completed_tasks)
        
        return {
            "completed": completed,
            "feedback": f"✅ All {len(completed_tasks)} completed tasks have QA tags" if completed else f"❌ {len(completed_tasks) - len(qa_tasks)} completed task(s) missing QA tags",
            "details": {"completed_total": len(completed_tasks), "with_qa": len(qa_tasks)}
        }
    
    def _validate_perfect_organization(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that all tasks are perfectly organized"""
        if len(tasks) == 0:
            return {
                "completed": False,
                "feedback": "❌ No tasks exist",
                "details": {}
            }
        
        perfectly_organized = [
            t for t in tasks
            if t.assigned_to and t.tags and len(t.tags) >= 2 and t.due_date
        ]
        
        completed = len(perfectly_organized) == len(tasks)
        
        return {
            "completed": completed,
            "feedback": f"✅ All {len(tasks)} tasks are perfectly organized" if completed else f"❌ {len(tasks) - len(perfectly_organized)} task(s) need: assignee, 2+ tags, and due date",
            "details": {"total_tasks": len(tasks), "organized": len(perfectly_organized)}
        }
    
    def _validate_reduce_wip(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that work-in-progress is limited"""
        wip_tasks = [t for t in tasks if t.status == "in_progress"]
        wip_count = len(wip_tasks)
        completed = wip_count <= 5
        
        return {
            "completed": completed,
            "feedback": f"✅ WIP limited to {wip_count} tasks" if completed else f"❌ Too much WIP: {wip_count} tasks (max: 5)",
            "details": {"wip_count": wip_count, "max_allowed": 5}
        }
    
    def _validate_feature_completion(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that all feature tasks are completed"""
        feature_tasks = [
            t for t in tasks
            if t.tags and 'feature' in [tag.lower() for tag in t.tags]
        ]
        
        if len(feature_tasks) == 0:
            return {
                "completed": True,
                "feedback": "✅ No feature tasks exist",
                "details": {}
            }
        
        completed_features = [t for t in feature_tasks if t.status == "completed"]
        completed = len(completed_features) == len(feature_tasks)
        
        return {
            "completed": completed,
            "feedback": f"✅ All {len(feature_tasks)} features completed" if completed else f"❌ {len(feature_tasks) - len(completed_features)} feature(s) still in progress",
            "details": {"total_features": len(feature_tasks), "completed": len(completed_features)}
        }
    
    def _validate_clean_slate(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that only archived tasks remain"""
        non_archived = [t for t in tasks if t.status != "archived"]
        completed = len(non_archived) == 0 and len(tasks) > 0
        
        return {
            "completed": completed,
            "feedback": "✅ Clean slate achieved - all tasks archived" if completed else f"❌ {len(non_archived)} task(s) still active (archive or complete them)",
            "details": {"non_archived_count": len(non_archived), "total_tasks": len(tasks)}
        }
    
    def _validate_milestone_achievement(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that 10+ tasks have been completed"""
        completed_tasks = [t for t in tasks if t.status == "completed"]
        count = len(completed_tasks)
        completed = count >= 10
        
        return {
            "completed": completed,
            "feedback": f"✅ Milestone! {count} tasks completed" if completed else f"❌ {count}/10 tasks completed",
            "details": {"completed_count": count, "target": 10}
        }
    
    def _validate_documentation_complete(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that all documentation tasks are completed"""
        doc_tasks = [
            t for t in tasks
            if t.tags and any('doc' in tag.lower() for tag in t.tags)
        ]
        
        if len(doc_tasks) == 0:
            return {
                "completed": True,
                "feedback": "✅ No documentation tasks exist",
                "details": {}
            }
        
        completed_docs = [t for t in doc_tasks if t.status == "completed"]
        completed = len(completed_docs) == len(doc_tasks)
        
        return {
            "completed": completed,
            "feedback": f"✅ All {len(doc_tasks)} documentation tasks completed" if completed else f"❌ {len(doc_tasks) - len(completed_docs)} documentation task(s) incomplete",
            "details": {"total_docs": len(doc_tasks), "completed": len(completed_docs)}
        }
    
    def _validate_no_low_priority_in_progress(self, tasks: List[Task]) -> Dict[str, Any]:
        """Validate that low priority tasks aren't in progress when high priority ones exist"""
        high_priority = [t for t in tasks if t.priority in ["high", "urgent"] and t.status == "todo"]
        low_in_progress = [t for t in tasks if t.priority == "low" and t.status == "in_progress"]
        
        # If there are high priority tasks waiting and low priority in progress, fail
        completed = len(high_priority) == 0 or len(low_in_progress) == 0
        
        return {
            "completed": completed,
            "feedback": "✅ Priority management optimal" if completed else f"❌ {len(low_in_progress)} low priority task(s) in progress while {len(high_priority)} high priority task(s) wait",
            "details": {
                "high_priority_waiting": len(high_priority),
                "low_priority_in_progress": len(low_in_progress)
            }
        }

