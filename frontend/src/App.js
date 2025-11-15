import React, { useState, useEffect } from 'react';
import './App.css';
import TaskBoard from './components/TaskBoard';
import RLDashboard from './components/RLDashboard';
import TaskForm from './components/TaskForm';
import { api } from './services/api';
import { Target, BarChart3, Plus } from 'lucide-react';

function App() {
  const [tasks, setTasks] = useState([]);
  const [rlState, setRlState] = useState(null);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [filterStatus, setFilterStatus] = useState('');
  const [filterPriority, setFilterPriority] = useState('');
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('tasks');

  useEffect(() => {
    loadData();
    // Refresh data every 5 seconds for demo purposes
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, [filterStatus, filterPriority]);

  const loadData = async () => {
    try {
      const [tasksData, stateData] = await Promise.all([
        api.getTasks(filterStatus, filterPriority),
        api.getRLState()
      ]);
      setTasks(tasksData);
      setRlState(stateData);
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      await api.createTask(taskData);
      setShowTaskForm(false);
      loadData();
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleUpdateTask = async (taskId, updates) => {
    try {
      await api.updateTask(taskId, updates);
      loadData();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await api.deleteTask(taskId);
      loadData();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleResetEnvironment = async () => {
    try {
      await api.resetEnvironment();
      loadData();
    } catch (error) {
      console.error('Error resetting environment:', error);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
        <p>Loading RL Environment...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <Target size={32} />
            <div>
              <h1>Task Management RL Environment</h1>
              <p className="subtitle">Training Environment for Computer-Use Agents</p>
            </div>
          </div>
          
          <div className="header-actions">
            <button 
              className="btn-primary"
              onClick={() => setShowTaskForm(true)}
            >
              <Plus size={20} />
              New Task
            </button>
          </div>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'tasks' ? 'active' : ''}`}
            onClick={() => setActiveTab('tasks')}
          >
            <Target size={18} />
            Task Board
          </button>
          <button
            className={`tab ${activeTab === 'rl' ? 'active' : ''}`}
            onClick={() => setActiveTab('rl')}
          >
            <BarChart3 size={18} />
            RL Dashboard
          </button>
        </div>
      </header>

      <main className="app-main">
        {activeTab === 'tasks' ? (
          <TaskBoard
            tasks={tasks}
            onUpdateTask={handleUpdateTask}
            onDeleteTask={handleDeleteTask}
            filterStatus={filterStatus}
            setFilterStatus={setFilterStatus}
            filterPriority={filterPriority}
            setFilterPriority={setFilterPriority}
          />
        ) : (
          <RLDashboard
            rlState={rlState}
            onReset={handleResetEnvironment}
          />
        )}
      </main>

      {showTaskForm && (
        <TaskForm
          onSubmit={handleCreateTask}
          onClose={() => setShowTaskForm(false)}
        />
      )}
    </div>
  );
}

export default App;

