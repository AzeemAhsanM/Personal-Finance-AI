
import axios from 'axios';

const api = axios.create({
  baseURL: "WealthFyBackend-env.eba-dmzp9vaa.eu-north-1.elasticbeanstalk.com",
});

api.interceptors.request.use((config) => {
  // Change 'access_token' to 'token' to match what you save during login
  const token = localStorage.getItem('token'); 
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;