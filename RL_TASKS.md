# RL Training Tasks

Complete reference for all 24 programmatically validated RL tasks.

## Task Categories

### Easy Tasks (10-20 points)

#### `create_urgent_task` - 10 points
- Objective: Create a task with 'urgent' priority
- Validation: At least one task with `priority="urgent"` exists

#### `complete_three_tasks` - 15 points
- Objective: Mark at least 3 tasks as completed
- Validation: Count of `status="completed"` >= 3

#### `assign_all_tasks` - 15 points
- Objective: Assign all unassigned tasks to team members
- Validation: No tasks with empty `assigned_to` field

#### `archive_completed` - 15 points
- Objective: Archive all completed tasks
- Validation: No tasks with `status="completed"` (should be "archived")

#### `documentation_complete` - 20 points
- Objective: Complete all documentation tasks
- Validation: All tasks with 'doc' tags have `status="completed"`

### Medium Tasks (20-25 points)

#### `organize_by_priority` - 20 points
- Objective: Ensure all high priority tasks are active
- Validation: No `priority="high"` tasks with `status="todo"`

#### `organize_with_tags` - 20 points
- Objective: Add at least 2 tags to every task
- Validation: All tasks have `len(tags) >= 2`

#### `prioritize_urgent_items` - 20 points
- Objective: Ensure all urgent tasks are in progress
- Validation: All `priority="urgent"` tasks have `status="in_progress"`

#### `reduce_wip` - 20 points
- Objective: Limit work-in-progress to 5 tasks
- Validation: Count of `status="in_progress"` <= 5

#### `quality_assurance` - 20 points
- Objective: Add QA tags to all completed tasks
- Validation: All completed tasks have QA-related tags ('tested', 'reviewed', 'qa', 'approved')

#### `balance_workload` - 25 points
- Objective: Distribute tasks evenly across team members
- Validation: Maximum difference between team members' task counts <= 2

#### `clear_overdue_tasks` - 25 points
- Objective: Complete or delete all overdue tasks
- Validation: No tasks with `due_date < now` and status not in [completed, archived]

#### `eliminate_technical_debt` - 25 points
- Objective: Resolve all technical debt tasks
- Validation: No active tasks with 'refactor' or 'technical-debt' tags

#### `deadline_management` - 25 points
- Objective: Manage tasks due within 3 days
- Validation: Tasks with `now <= due_date <= now + 3 days` must be in_progress or completed

#### `no_low_priority_in_progress` - 25 points
- Objective: Optimize priority management
- Validation: If high/urgent tasks are todo, no low priority tasks should be in progress

### Hard Tasks (30-35 points)

#### `achieve_80_completion` - 30 points
- Objective: Reach 80% completion rate
- Validation: `(completed_tasks / total_tasks) * 100 >= 80.0`

#### `create_sprint_backlog` - 30 points
- Objective: Create 5+ sprint tasks
- Validation: Count of tasks with 'sprint' tags and `assigned_to` not null >= 5

#### `optimize_task_flow` - 30 points
- Objective: Balance pipeline
- Validation: `count(todo) < count(in_progress) < count(completed)`

#### `feature_completion` - 30 points
- Objective: Complete all feature tasks
- Validation: All tasks with 'feature' tag have `status="completed"`

#### `achieve_zero_bugs` - 35 points
- Objective: Resolve all bug tasks
- Validation: No active tasks with 'bug' tag

#### `perfect_organization` - 35 points
- Objective: Fully organize all tasks
- Validation: All tasks have assignee, 2+ tags, and due date

### Very Hard Tasks (40-50 points)

#### `team_collaboration` - 40 points
- Objective: Ensure team-wide task distribution
- Validation: Each team member has tasks in todo, in_progress, and completed statuses

#### `milestone_achievement` - 40 points
- Objective: Complete 10+ tasks in single episode
- Validation: Count of `status="completed"` >= 10

#### `clean_slate` - 50 points
- Objective: Archive everything
- Validation: All tasks have `status="archived"` and at least one task exists

## Validation Details

All tasks provide:
- Programmatic validation (no human required)
- Clear success criteria
- Immediate reward feedback
- Detailed status information

## Total Rewards

- Easy: 75 points (5 tasks)
- Medium: 230 points (10 tasks)
- Hard: 190 points (6 tasks)
- Very Hard: 130 points (3 tasks)
- **Total: 585 points**

## Integration

See [AGENT_INTEGRATION.md](./AGENT_INTEGRATION.md) for:
- Code examples using these tasks
- State/action space design
- Reward shaping strategies
- Training implementation
