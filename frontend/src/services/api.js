import axios from 'axios';

// Read API Base URL from configurable environment variable, defaulting to standard backend port
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080/api';

// In-memory token storage (Strictly NO localStorage per security requirements)
let inMemoryToken = null;

export const setAuthToken = (token) => {
  inMemoryToken = token;
};

export const getAuthToken = () => {
  return inMemoryToken;
};

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Accept': 'application/json',
  },
});

// Request interceptor: Attach JWT Bearer token from in-memory state
apiClient.interceptors.request.use(
  (config) => {
    if (inMemoryToken) {
      config.headers.Authorization = `Bearer ${inMemoryToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: Clear in-memory token on 401 Unauthorized
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      inMemoryToken = null;
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (email, password) => {
    const response = await apiClient.post('/auth/login', { email, password });
    if (response.data && response.data.token) {
      setAuthToken(response.data.token);
    }
    return response.data;
  },

  register: async (email, password, fullName) => {
    const response = await apiClient.post('/auth/register', { email, password, fullName });
    if (response.data && response.data.token) {
      setAuthToken(response.data.token);
    }
    return response.data;
  },

  logout: () => {
    setAuthToken(null);
  },
};

export const videoApi = {
  uploadSingle: async (file, preset, targetFormat, onUploadProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('preset', preset);
    if (targetFormat) {
      formData.append('format', targetFormat);
    }

    const response = await apiClient.post('/videos/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress,
    });
    return response.data;
  },

  uploadBatch: async (files, preset, targetFormat, onUploadProgress) => {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    formData.append('preset', preset);
    if (targetFormat) {
      formData.append('format', targetFormat);
    }

    const response = await apiClient.post('/videos/upload-batch', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress,
    });
    return response.data;
  },

  getJobs: async (page = 0, size = 10, status = 'ALL') => {
    const response = await apiClient.get('/videos/jobs', {
      params: { page, size, status },
    });
    return response.data;
  },

  getJob: async (id) => {
    const response = await apiClient.get(`/videos/jobs/${id}`);
    return response.data;
  },

  retryJob: async (id) => {
    const response = await apiClient.post(`/videos/jobs/${id}/retry`);
    return response.data;
  },

  getStats: async () => {
    const response = await apiClient.get('/videos/stats');
    return response.data;
  },

  downloadCompressedVideo: async (jobId, originalFileName) => {
    const response = await apiClient.get(`/videos/jobs/${jobId}/download`, {
      responseType: 'blob',
    });

    const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = blobUrl;
    link.setAttribute('download', `compressed_${originalFileName}`);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);
  },
};

export const healthApi = {
  checkHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default apiClient;
