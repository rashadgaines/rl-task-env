import React from 'react';
import './TaskBoard.css';
import TaskCard from './TaskCard';
import { Filter } from 'lucide-react';

const TaskBoard = ({ 
  tasks, 
  onUpdateTask, 
  onDeleteTask,
  filterStatus,
  setFilterStatus,
  filterPriority,
  setFilterPriority
}) => {
  const statuses = [
    { value: '', label: 'All' },
    { value: 'todo', label: 'To Do' },
    { value: 'in_progress', label: 'In Progress' },
    { value: 'completed', label: 'Completed' },
    { value: 'archived', label: 'Archived' }
  ];

  const priorities = [
    { value: '', label: 'All' },
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
    { value: 'urgent', label: 'Urgent' }
  ];

  const groupedTasks = {
    todo: tasks.filter(t => t.status === 'todo'),
    in_progress: tasks.filter(t => t.status === 'in_progress'),
    completed: tasks.filter(t => t.status === 'completed'),
    archived: tasks.filter(t => t.status === 'archived')
  };

  return (
    <div className="task-board">
      <div className="board-filters">
        <div className="filter-group">
          <Filter size={16} />
          <span>Filters:</span>
          
          <select 
            value={filterStatus} 
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filter-select"
          >
            {statuses.map(s => (
              <option key={s.value} value={s.value}>{s.label}</option>
            ))}
          </select>

          <select 
            value={filterPriority} 
            onChange={(e) => setFilterPriority(e.target.value)}
            className="filter-select"
          >
            {priorities.map(p => (
              <option key={p.value} value={p.value}>
                {p.label} Priority
              </option>
            ))}
          </select>
        </div>

        <div className="task-count">
          {tasks.length} task{tasks.length !== 1 ? 's' : ''}
        </div>
      </div>

      <div className="board-columns">
        <div className="board-column">
          <div className="column-header todo-header">
            <h3>To Do</h3>
            <span className="count">{groupedTasks.todo.length}</span>
          </div>
          <div className="column-content">
            {groupedTasks.todo.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onUpdate={onUpdateTask}
                onDelete={onDeleteTask}
              />
            ))}
          </div>
        </div>

        <div className="board-column">
          <div className="column-header progress-header">
            <h3>In Progress</h3>
            <span className="count">{groupedTasks.in_progress.length}</span>
          </div>
          <div className="column-content">
            {groupedTasks.in_progress.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onUpdate={onUpdateTask}
                onDelete={onDeleteTask}
              />
            ))}
          </div>
        </div>

        <div className="board-column">
          <div className="column-header completed-header">
            <h3>Completed</h3>
            <span className="count">{groupedTasks.completed.length}</span>
          </div>
          <div className="column-content">
            {groupedTasks.completed.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onUpdate={onUpdateTask}
                onDelete={onDeleteTask}
              />
            ))}
          </div>
        </div>

        <div className="board-column">
          <div className="column-header archived-header">
            <h3>Archived</h3>
            <span className="count">{groupedTasks.archived.length}</span>
          </div>
          <div className="column-content">
            {groupedTasks.archived.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onUpdate={onUpdateTask}
                onDelete={onDeleteTask}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskBoard;

