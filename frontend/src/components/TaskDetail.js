import React, { useState } from 'react';
import './TaskDetail.css';
import { X, Calendar, User, Tag, Clock, Edit2, Trash2 } from 'lucide-react';

const TaskDetail = ({ task, onClose, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTask, setEditedTask] = useState({
    title: task.title,
    description: task.description,
    status: task.status,
    priority: task.priority,
    assigned_to: task.assigned_to || '',
    tags: task.tags ? task.tags.join(', ') : '',
  });

  const priorityColors = {
    low: '#48bb78',
    medium: '#ed8936',
    high: '#f56565',
    urgent: '#e53e3e'
  };

  const statusColors = {
    todo: '#667eea',
    in_progress: '#f093fb',
    completed: '#4facfe',
    archived: '#43e97b'
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    const now = new Date();
    const isOverdue = date < now && task.status !== 'completed' && task.status !== 'archived';
    
    return {
      formatted: date.toLocaleDateString('en-US', { 
        weekday: 'long',
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }),
      isOverdue
    };
  };

  const formatRelativeDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = date - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return `${Math.abs(diffDays)} days overdue`;
    if (diffDays === 0) return 'Due today';
    if (diffDays === 1) return 'Due tomorrow';
    return `Due in ${diffDays} days`;
  };

  const dueDate = formatDate(task.due_date);
  const relativeDueDate = formatRelativeDate(task.due_date);
  const createdDate = formatDate(task.created_at);
  const updatedDate = formatDate(task.updated_at);

  const handleSave = () => {
    const updates = {
      title: editedTask.title,
      description: editedTask.description,
      status: editedTask.status,
      priority: editedTask.priority,
      assigned_to: editedTask.assigned_to || null,
      tags: editedTask.tags ? editedTask.tags.split(',').map(t => t.trim()).filter(t => t) : [],
    };
    onUpdate(task.id, updates);
    setIsEditing(false);
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      onDelete(task.id);
      onClose();
    }
  };

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="task-detail-overlay" onClick={handleBackdropClick}>
      <div className="task-detail-modal">
        {/* Header */}
        <div className="task-detail-header" style={{ 
          background: `linear-gradient(135deg, ${statusColors[task.status]} 0%, ${priorityColors[task.priority]} 100%)`
        }}>
          <div className="task-detail-header-content">
            <div className="task-detail-badges">
              <span className="status-badge">{task.status.replace('_', ' ')}</span>
              <span 
                className="priority-badge"
                style={{ backgroundColor: priorityColors[task.priority] }}
              >
                {task.priority} priority
              </span>
            </div>
            <div className="task-detail-actions">
              {!isEditing && (
                <button 
                  className="detail-action-btn"
                  onClick={() => setIsEditing(true)}
                  title="Edit task"
                >
                  <Edit2 size={18} />
                </button>
              )}
              <button 
                className="detail-action-btn delete"
                onClick={handleDelete}
                title="Delete task"
              >
                <Trash2 size={18} />
              </button>
              <button 
                className="detail-action-btn"
                onClick={onClose}
                title="Close"
              >
                <X size={20} />
              </button>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="task-detail-content">
          {isEditing ? (
            <div className="task-detail-edit">
              <div className="edit-field">
                <label>Title</label>
                <input
                  type="text"
                  value={editedTask.title}
                  onChange={(e) => setEditedTask({ ...editedTask, title: e.target.value })}
                  placeholder="Task title"
                />
              </div>

              <div className="edit-field">
                <label>Description</label>
                <textarea
                  value={editedTask.description}
                  onChange={(e) => setEditedTask({ ...editedTask, description: e.target.value })}
                  placeholder="Task description"
                  rows={5}
                />
              </div>

              <div className="edit-row">
                <div className="edit-field">
                  <label>Status</label>
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
                  <label>Priority</label>
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
              </div>

              <div className="edit-field">
                <label>Assigned To</label>
                <input
                  type="text"
                  value={editedTask.assigned_to}
                  onChange={(e) => setEditedTask({ ...editedTask, assigned_to: e.target.value })}
                  placeholder="Assignee name"
                />
              </div>

              <div className="edit-field">
                <label>Tags (comma separated)</label>
                <input
                  type="text"
                  value={editedTask.tags}
                  onChange={(e) => setEditedTask({ ...editedTask, tags: e.target.value })}
                  placeholder="bug, frontend, urgent"
                />
              </div>

              <div className="edit-actions">
                <button className="btn-cancel-edit" onClick={() => setIsEditing(false)}>
                  Cancel
                </button>
                <button className="btn-save-edit" onClick={handleSave}>
                  Save Changes
                </button>
              </div>
            </div>
          ) : (
            <>
              <h2 className="task-detail-title">{task.title}</h2>
              
              {task.description && (
                <div className="task-detail-section">
                  <h3>Description</h3>
                  <p className="task-description-text">{task.description}</p>
                </div>
              )}

              <div className="task-detail-grid">
                <div className="detail-item">
                  <div className="detail-icon">
                    <User size={20} />
                  </div>
                  <div className="detail-content">
                    <div className="detail-label">Assigned To</div>
                    <div className="detail-value">
                      {task.assigned_to || <span className="text-muted">Unassigned</span>}
                    </div>
                  </div>
                </div>

                <div className="detail-item">
                  <div className="detail-icon">
                    <Calendar size={20} />
                  </div>
                  <div className="detail-content">
                    <div className="detail-label">Due Date</div>
                    <div className={`detail-value ${dueDate.isOverdue ? 'overdue' : ''}`}>
                      {dueDate.formatted}
                      {relativeDueDate && (
                        <span className={`relative-date ${dueDate.isOverdue ? 'overdue' : ''}`}>
                          {relativeDueDate}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {task.tags && task.tags.length > 0 && (
                  <div className="detail-item full-width">
                    <div className="detail-icon">
                      <Tag size={20} />
                    </div>
                    <div className="detail-content">
                      <div className="detail-label">Tags</div>
                      <div className="detail-tags">
                        {task.tags.map((tag, index) => (
                          <span key={index} className="detail-tag">{tag}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                <div className="detail-item">
                  <div className="detail-icon">
                    <Clock size={20} />
                  </div>
                  <div className="detail-content">
                    <div className="detail-label">Created</div>
                    <div className="detail-value-small">{createdDate.formatted}</div>
                  </div>
                </div>

                <div className="detail-item">
                  <div className="detail-icon">
                    <Clock size={20} />
                  </div>
                  <div className="detail-content">
                    <div className="detail-label">Last Updated</div>
                    <div className="detail-value-small">{updatedDate.formatted}</div>
                  </div>
                </div>
              </div>

              <div className="task-detail-footer">
                <div className="task-id">Task ID: #{task.id}</div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskDetail;

