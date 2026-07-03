import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Get all assets
  getAssets: async (resourceType = null) => {
    const params = resourceType ? { resource_type: resourceType } : {};
    const response = await api.get('/assets', { params });
    return response.data;
  },

  // Get single asset
  getAsset: async (assetId) => {
    const response = await api.get(`/assets/${assetId}`);
    return response.data;
  },

  // Get all agents
  getAgents: async (minConfidence = 0) => {
    const response = await api.get('/agents', {
      params: { min_confidence: minConfidence }
    });
    return response.data;
  },

  // Get single agent
  getAgent: async (agentId) => {
    const response = await api.get(`/agents/${agentId}`);
    return response.data;
  },

  // Trigger scan
  triggerScan: async (projectId = null) => {
    const data = projectId ? { project_id: projectId } : {};
    const response = await api.post('/scan', data);
    return response.data;
  },

  // Get scan status
  getScanStatus: async (scanId) => {
    const response = await api.get(`/scans/${scanId}`);
    return response.data;
  },

  // Get statistics
  getStatistics: async () => {
    const response = await api.get('/stats');
    return response.data;
  },
};

export default apiService;
