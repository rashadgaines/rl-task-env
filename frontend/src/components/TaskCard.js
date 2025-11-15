import React, { useState } from 'react';
import './TaskCard.css';
import { Calendar, User, Tag, Trash2, Edit2 } from 'lucide-react';
import TaskDetail from './TaskDetail';

const TaskCard = ({ task, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [showDetail, setShowDetail] = useState(false);
  const [editedTask, setEditedTask] = useState({
    status: task.status,
    priority: task.priority,
  });

  const priorityColors = {
    low: '#48bb78',
    medium: '#ed8936',
    high: '#f56565',
    urgent: '#e53e3e'
  };

  const formatDate = (dateString) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    const now = new Date();
    const isOverdue = date < now && task.status !== 'completed' && task.status !== 'archived';
    
    return {
      formatted: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      isOverdue
    };
  };

  const dueDate = formatDate(task.due_date);

  const handleSaveEdit = () => {
    onUpdate(task.id, editedTask);
    setIsEditing(false);
  };

  const handleCardClick = (e) => {
    // Don't open detail if clicking on action buttons
    if (e.target.closest('.task-actions') || e.target.closest('.task-edit')) {
      return;
    }
    setShowDetail(true);
  };

  return (
    <>
      <div className="task-card" onClick={handleCardClick}>
        <div className="task-card-header">
          <div 
            className="priority-indicator" 
            style={{ backgroundColor: priorityColors[task.priority] }}
            title={`${task.priority} priority`}
          />
          <div className="task-actions">
            <button 
              className="icon-btn"
              onClick={(e) => {
                e.stopPropagation();
                setIsEditing(!isEditing);
              }}
              title="Edit task"
            >
              <Edit2 size={14} />
            </button>
            <button 
              className="icon-btn delete-btn"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(task.id);
              }}
              title="Delete task"
            >
              <Trash2 size={14} />
            </button>
          </div>
        </div>

        <h4 className="task-title">{task.title}</h4>
      
      {task.description && (
        <p className="task-description">{task.description}</p>
      )}

      {isEditing ? (
        <div className="task-edit">
          <div className="edit-field">
            <label>Status:</label>
            <select
              value={editedTask.status}
              onChange={(e) => setEditedTask({ ...editedTask, status: e.target.value })}
            >
              <option value="todo">To Do</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="archived">Archived</option>
            </select>
          </div>

          <div className="edit-field">
            <label>Priority:</label>
            <select
              value={editedTask.priority}
              onChange={(e) => setEditedTask({ ...editedTask, priority: e.target.value })}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>

          <button className="btn-save" onClick={handleSaveEdit}>
            Save Changes
          </button>
        </div>
      ) : (
        <div className="task-meta">
          {task.assigned_to && (
            <div className="meta-item">
              <User size={14} />
              <span>{task.assigned_to}</span>
            </div>
          )}

          {dueDate && (
            <div className={`meta-item ${dueDate.isOverdue ? 'overdue' : ''}`}>
              <Calendar size={14} />
              <span>{dueDate.formatted}</span>
            </div>
          )}

          {task.tags && task.tags.length > 0 && (
            <div className="task-tags">
              <Tag size={14} />
              {task.tags.slice(0, 3).map((tag, index) => (
                <span key={index} className="tag">{tag}</span>
              ))}
            </div>
          )}
        </div>
      )}
      </div>

      {showDetail && (
        <TaskDetail
          task={task}
          onClose={() => setShowDetail(false)}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      )}
    </>
  );
};

export default TaskCard;

