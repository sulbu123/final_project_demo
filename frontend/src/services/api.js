import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 - 토큰 추가
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터 - 에러 처리
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
};

export const quizAPI = {
  getQuizzes: () => api.get('/quiz'),
  getQuiz: (id) => api.get(`/quiz/${id}`),
  createQuiz: (quizData) => api.post('/quiz', quizData),
  submitAnswer: (quizId, answer) => api.post(`/quiz/${quizId}/answer`, { answer }),
  generateAIQuiz: (videoFile, category) => {
    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('category', category);
    return api.post('/quiz/generate', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const analysisAPI = {
  getUserStats: () => api.get('/analysis/stats'),
  getWrongAnswers: () => api.get('/analysis/wrong-answers'),
  getLearningProgress: () => api.get('/analysis/progress'),
};

export const userAPI = {
  getProfile: () => api.get('/user/profile'),
  updateProfile: (userData) => api.put('/user/profile', userData),
};

export default api; 