import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Task endpoints
  getTasks: async (status = '', priority = '') => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (priority) params.append('priority', priority);
    const response = await apiClient.get(`/api/tasks?${params.toString()}`);
    return response.data;
  },

  getTask: async (taskId) => {
    const response = await apiClient.get(`/api/tasks/${taskId}`);
    return response.data;
  },

  createTask: async (taskData) => {
    const response = await apiClient.post('/api/tasks', taskData);
    return response.data;
  },

  updateTask: async (taskId, updates) => {
    const response = await apiClient.put(`/api/tasks/${taskId}`, updates);
    return response.data;
  },

  deleteTask: async (taskId) => {
    const response = await apiClient.delete(`/api/tasks/${taskId}`);
    return response.data;
  },

  // RL endpoints
  getRLState: async () => {
    const response = await apiClient.get('/api/rl/state');
    return response.data;
  },

  getRLTasks: async () => {
    const response = await apiClient.get('/api/rl/tasks');
    return response.data;
  },

  validateRLTask: async (taskName) => {
    const response = await apiClient.post(`/api/rl/validate/${taskName}`);
    return response.data;
  },

  resetEnvironment: async () => {
    const response = await apiClient.post('/api/rl/reset');
    return response.data;
  },
};

