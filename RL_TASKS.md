# RL Training Tasks - Complete Guide

This document provides a comprehensive overview of all 24 programmatically validated RL tasks in the environment.

## 🎯 Task Categories

### 1. Basic Operations (Easy - 10-20 points)
Foundation tasks that test basic agent capabilities.

#### `create_urgent_task` - 10 points ⭐ Easy
**Objective:** Create a new task with 'urgent' priority  
**Validation:** Checks if at least one task with `priority="urgent"` exists  
**Skills Tested:** Task creation, priority setting

#### `complete_three_tasks` - 15 points ⭐ Easy
**Objective:** Mark at least 3 tasks as completed  
**Validation:** Counts tasks with `status="completed"`, requires ≥3  
**Skills Tested:** Task status manipulation, goal achievement

#### `assign_all_tasks` - 15 points ⭐ Easy
**Objective:** Assign all unassigned tasks to team members  
**Validation:** Ensures no tasks have empty `assigned_to` field  
**Skills Tested:** Team management, assignment logic

#### `archive_completed` - 15 points ⭐ Easy
**Objective:** Archive all completed tasks to clean up the board  
**Validation:** No tasks should have `status="completed"` (should be "archived")  
**Skills Tested:** Board cleanup, workflow management

#### `documentation_complete` - 20 points ⭐ Easy
**Objective:** Complete all tasks tagged with 'documentation'  
**Validation:** All tasks with 'doc' tags must have `status="completed"`  
**Skills Tested:** Tag filtering, targeted completion

---

### 2. Organization & Workflow (Medium - 20-25 points)
Tasks requiring strategic thinking and organization.

#### `organize_by_priority` - 20 points ⭐⭐ Medium
**Objective:** Ensure all high priority tasks are either in_progress or completed  
**Validation:** No tasks with `priority="high"` should have `status="todo"`  
**Skills Tested:** Priority management, workflow optimization

#### `organize_with_tags` - 20 points ⭐⭐ Medium
**Objective:** Add at least 2 tags to every task  
**Validation:** All tasks must have `len(tags) >= 2`  
**Skills Tested:** Metadata management, organization

#### `prioritize_urgent_items` - 20 points ⭐⭐ Medium
**Objective:** Ensure all urgent tasks are in_progress  
**Validation:** All tasks with `priority="urgent"` must have `status="in_progress"`  
**Skills Tested:** Urgency handling, status management

#### `reduce_wip` - 20 points ⭐⭐ Medium
**Objective:** Reduce work-in-progress to maximum 5 tasks  
**Validation:** Count of tasks with `status="in_progress"` must be ≤5  
**Skills Tested:** WIP limits, lean methodology

#### `quality_assurance` - 20 points ⭐⭐ Medium
**Objective:** Add 'tested' or 'reviewed' tags to all completed tasks  
**Validation:** All completed tasks must have QA-related tags  
**Skills Tested:** Quality control, validation processes

#### `balance_workload` - 25 points ⭐⭐ Medium
**Objective:** Distribute tasks evenly across team members  
**Validation:** Maximum difference between team members' task counts ≤2  
**Skills Tested:** Load balancing, resource optimization

#### `clear_overdue_tasks` - 25 points ⭐⭐ Medium
**Objective:** Complete or delete all tasks with past due dates  
**Validation:** No tasks with `due_date < now` and status not in [completed, archived]  
**Skills Tested:** Deadline management, time awareness

#### `eliminate_technical_debt` - 25 points ⭐⭐ Medium
**Objective:** Complete or archive all tasks tagged with 'refactor' or 'technical-debt'  
**Validation:** No active tasks with technical debt tags  
**Skills Tested:** Codebase health, maintenance priorities

#### `deadline_management` - 25 points ⭐⭐ Medium
**Objective:** Ensure all tasks due within 3 days are in_progress or completed  
**Validation:** Tasks with `now <= due_date <= now + 3 days` must be active  
**Skills Tested:** Proactive planning, time management

#### `no_low_priority_in_progress` - 25 points ⭐⭐ Medium
**Objective:** Ensure no low priority tasks are in_progress when high priority tasks exist  
**Validation:** If high/urgent tasks are in todo, no low priority tasks should be in progress  
**Skills Tested:** Priority optimization, resource allocation

---

### 3. Advanced Goals (Hard - 30-35 points)
Complex tasks requiring multi-step reasoning.

#### `achieve_80_completion` - 30 points ⭐⭐⭐ Hard
**Objective:** Achieve at least 80% task completion rate  
**Validation:** `(completed_tasks / total_tasks) * 100 >= 80.0`  
**Skills Tested:** Goal achievement, completion optimization

#### `create_sprint_backlog` - 30 points ⭐⭐⭐ Hard
**Objective:** Create at least 5 new tasks with 'sprint' tags and assign them  
**Validation:** Count tasks with 'sprint' in tags and `assigned_to` not null, requires ≥5  
**Skills Tested:** Sprint planning, task creation at scale

#### `optimize_task_flow` - 30 points ⭐⭐⭐ Hard
**Objective:** Balance pipeline so todo < in_progress < completed  
**Validation:** `count(todo) < count(in_progress) < count(completed)`  
**Skills Tested:** Pipeline optimization, workflow theory

#### `feature_completion` - 30 points ⭐⭐⭐ Hard
**Objective:** Complete all tasks tagged with 'feature'  
**Validation:** All tasks with 'feature' tag must have `status="completed"`  
**Skills Tested:** Feature delivery, completion focus

#### `achieve_zero_bugs` - 35 points ⭐⭐⭐ Hard
**Objective:** Complete or delete all tasks tagged with 'bug'  
**Validation:** No active tasks with 'bug' tag  
**Skills Tested:** Bug triage, quality achievement

#### `perfect_organization` - 35 points ⭐⭐⭐ Hard
**Objective:** All tasks must have assignee, 2+ tags, and due date  
**Validation:** Every task must have all three attributes populated  
**Skills Tested:** Complete organization, attention to detail

---

### 4. Expert Challenges (Very Hard - 40-50 points)
Ultimate challenges requiring sophisticated strategies.

#### `team_collaboration` - 40 points ⭐⭐⭐⭐ Very Hard
**Objective:** Ensure every team member has at least one task in each status category  
**Validation:** For each unique assignee, they must have tasks in todo, in_progress, and completed  
**Skills Tested:** Multi-agent coordination, comprehensive team management

#### `milestone_achievement` - 40 points ⭐⭐⭐⭐ Very Hard
**Objective:** Complete at least 10 tasks in a single episode  
**Validation:** Count of tasks with `status="completed"` must be ≥10  
**Skills Tested:** High-volume completion, efficiency

#### `clean_slate` - 50 points ⭐⭐⭐⭐ Very Hard
**Objective:** Archive or complete all tasks - only archived tasks should remain  
**Validation:** All tasks must have `status="archived"` and at least one task must exist  
**Skills Tested:** Complete cleanup, thorough execution

---

## 📊 Task Difficulty Distribution

```
Easy (5 tasks):        █████ 21%
Medium (10 tasks):     ██████████ 42%
Hard (6 tasks):        ██████ 25%
Very Hard (3 tasks):   ███ 12%
```

## 🎮 Reward Structure

**Total Possible Rewards:** 585 points (if all tasks completed)

**Reward Distribution:**
- Easy tasks: 75 points (13%)
- Medium tasks: 230 points (39%)
- Hard tasks: 190 points (32%)
- Very Hard tasks: 130 points (22%)

**Progressive difficulty ensures:**
- ✅ Easy entry for learning
- ✅ Challenging mid-tier goals
- ✅ Expert-level accomplishments
- ✅ Clear skill progression

## 🔬 Agent Skills Required

### Core Skills
1. **CRUD Operations** - Create, Read, Update, Delete tasks
2. **Filtering & Querying** - Find specific tasks by attributes
3. **Status Management** - Update task states appropriately
4. **Priority Handling** - Understand and act on priority levels
5. **Tag Management** - Add, read, and filter by tags
6. **Assignment Logic** - Distribute work to team members

### Advanced Skills
7. **Temporal Reasoning** - Handle due dates and deadlines
8. **Optimization** - Balance workloads and pipelines
9. **Pattern Recognition** - Identify task categories
10. **Multi-step Planning** - Coordinate multiple actions
11. **Constraint Satisfaction** - Meet multiple requirements simultaneously
12. **Resource Allocation** - Distribute limited resources

### Expert Skills
13. **Multi-agent Coordination** - Manage entire teams
14. **Strategic Planning** - Long-term goal achievement
15. **Complete Execution** - Thorough task completion
16. **Quality Control** - Ensure standards are met

## 🧪 Testing Strategies

### For Agent Developers

**Beginner Level:**
```python
# Test basic operations
tasks = ["create_urgent_task", "complete_three_tasks", "assign_all_tasks"]
```

**Intermediate Level:**
```python
# Test organization and workflow
tasks = ["organize_by_priority", "reduce_wip", "deadline_management"]
```

**Advanced Level:**
```python
# Test complex goals
tasks = ["achieve_80_completion", "optimize_task_flow", "achieve_zero_bugs"]
```

**Expert Level:**
```python
# Test ultimate challenges
tasks = ["team_collaboration", "clean_slate", "milestone_achievement"]
```

## 🎯 Training Scenarios

### Scenario 1: Sprint Planning
Focus on: `create_sprint_backlog`, `balance_workload`, `deadline_management`

### Scenario 2: Bug Bash
Focus on: `achieve_zero_bugs`, `prioritize_urgent_items`, `quality_assurance`

### Scenario 3: Technical Debt Cleanup
Focus on: `eliminate_technical_debt`, `feature_completion`, `documentation_complete`

### Scenario 4: Perfect Organization
Focus on: `perfect_organization`, `organize_with_tags`, `assign_all_tasks`

### Scenario 5: Final Delivery
Focus on: `achieve_80_completion`, `clean_slate`, `milestone_achievement`

## 💡 Best Practices for Agents

1. **Start with Easy Tasks** - Build confidence and understanding
2. **Read Task Requirements Carefully** - Validation is strict
3. **Plan Multi-step Actions** - Some tasks require coordination
4. **Check Current State First** - Use `/api/rl/state` endpoint
5. **Validate Frequently** - Get immediate feedback
6. **Learn from Failures** - Feedback messages provide guidance
7. **Reset When Needed** - Use `/api/rl/reset` for fresh start

## 🔧 For Environment Developers

### Adding New Tasks

```python
# In backend/rl_validator.py

# 1. Add to _define_rl_tasks()
"my_new_task": RLTask(
    name="my_new_task",
    description="Clear description of what to achieve",
    validation_fn=self._validate_my_new_task,
    reward=25.0,
    difficulty="medium"
),

# 2. Implement validation function
def _validate_my_new_task(self, tasks: List[Task]) -> Dict[str, Any]:
    # Your validation logic here
    completed = # boolean condition
    
    return {
        "completed": completed,
        "feedback": "Success/failure message",
        "details": {"key": "value"}
    }
```

## 📈 Success Metrics

**For Benchmarking Agents:**

- **Task Completion Rate** - How many tasks can be completed?
- **Average Reward per Episode** - Efficiency measure
- **Actions per Completed Task** - Efficiency metric
- **Difficult Task Success Rate** - Advanced capability measure
- **Time to Complete All Tasks** - Speed metric

## 🏆 Challenge Modes

### Speed Run
Complete as many tasks as possible in minimum actions.

### Perfect Score
Complete all 24 tasks in a single episode.

### Efficiency Challenge
Maximize reward per action taken.

### Difficulty Ladder
Complete tasks in order of difficulty (easy → very hard).

---

**This comprehensive task set demonstrates deep RL environment design expertise and provides rich training opportunities for computer-use agents!** 🚀

