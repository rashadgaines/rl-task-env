import React, { useState, useEffect } from 'react';
import './RLDashboard.css';
import { api } from '../services/api';
import { 
  Activity, 
  Award, 
  Target, 
  TrendingUp, 
  CheckCircle, 
  RefreshCw,
  Zap 
} from 'lucide-react';

const RLDashboard = ({ rlState, onReset }) => {
  const [rlTasks, setRlTasks] = useState([]);
  const [validationResults, setValidationResults] = useState({});
  const [validating, setValidating] = useState({});

  useEffect(() => {
    loadRLTasks();
  }, []);

  const loadRLTasks = async () => {
    try {
      const tasks = await api.getRLTasks();
      setRlTasks(tasks);
    } catch (error) {
      console.error('Error loading RL tasks:', error);
    }
  };

  const handleValidateTask = async (taskName) => {
    setValidating({ ...validating, [taskName]: true });
    try {
      const result = await api.validateRLTask(taskName);
      setValidationResults({ ...validationResults, [taskName]: result });
    } catch (error) {
      console.error('Error validating task:', error);
    } finally {
      setValidating({ ...validating, [taskName]: false });
    }
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: '#48bb78',
      medium: '#ed8936',
      hard: '#e53e3e',
      very_hard: '#9333ea'
    };
    return colors[difficulty] || '#718096';
  };

  if (!rlState) {
    return <div className="rl-dashboard">Loading...</div>;
  }

  return (
    <div className="rl-dashboard">
      <div className="dashboard-header">
        <h2>Reinforcement Learning Environment</h2>
        <button className="btn-reset" onClick={onReset}>
          <RefreshCw size={18} />
          Reset Environment
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
            <Target size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-label">Total Tasks</p>
            <p className="stat-value">{rlState.total_tasks}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
            <Activity size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-label">Actions Taken</p>
            <p className="stat-value">{rlState.actions_taken}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-label">Completion Rate</p>
            <p className="stat-value">{rlState.completion_rate.toFixed(1)}%</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' }}>
            <Award size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-label">Total Reward</p>
            <p className="stat-value">{rlState.current_reward.toFixed(1)}</p>
          </div>
        </div>
      </div>

      <div className="dashboard-sections">
        <div className="section">
          <h3>Task Distribution</h3>
          <div className="distribution-grid">
            <div className="distribution-card">
              <h4>By Status</h4>
              <div className="distribution-list">
                {Object.entries(rlState.tasks_by_status).map(([status, count]) => (
                  <div key={status} className="distribution-item">
                    <span className="distribution-label">{status.replace('_', ' ')}</span>
                    <span className="distribution-value">{count}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="distribution-card">
              <h4>By Priority</h4>
              <div className="distribution-list">
                {Object.entries(rlState.tasks_by_priority).map(([priority, count]) => (
                  <div key={priority} className="distribution-item">
                    <span className="distribution-label">{priority}</span>
                    <span className="distribution-value">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="section">
          <h3>
            <Zap size={20} />
            Available RL Tasks
          </h3>
          <p className="section-description">
            These are programmatically validated tasks that agents can attempt to complete for rewards.
          </p>
          
          <div className="rl-tasks-grid">
            {rlTasks.map((task) => {
              const result = validationResults[task.name];
              const isValidating = validating[task.name];

              return (
                <div key={task.name} className="rl-task-card">
                  <div className="rl-task-header">
                    <div className="rl-task-info">
                      <h4>{task.name.replace(/_/g, ' ')}</h4>
                      <span 
                        className="difficulty-badge"
                        style={{ backgroundColor: getDifficultyColor(task.difficulty) }}
                      >
                        {task.difficulty}
                      </span>
                    </div>
                    <div className="reward-badge">
                      <Award size={16} />
                      +{task.reward}
                    </div>
                  </div>

                  <p className="rl-task-description">{task.description}</p>

                  <button
                    className="btn-validate"
                    onClick={() => handleValidateTask(task.name)}
                    disabled={isValidating}
                  >
                    {isValidating ? (
                      'Validating...'
                    ) : (
                      <>
                        <CheckCircle size={16} />
                        Validate
                      </>
                    )}
                  </button>

                  {result && (
                    <div className={`validation-result ${result.completed ? 'success' : 'failure'}`}>
                      <div className="result-header">
                        {result.completed ? '✅ Completed!' : '❌ Not Completed'}
                        {result.completed && (
                          <span className="reward-earned">+{result.reward} points</span>
                        )}
                      </div>
                      <p className="result-feedback">{result.feedback}</p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="episode-info">
        <p>Episode #{rlState.episode_number}</p>
      </div>
    </div>
  );
};

export default RLDashboard;

