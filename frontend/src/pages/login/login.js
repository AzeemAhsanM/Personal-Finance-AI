import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../api'
import logo from './../../assets/logo.png';
import './login.css';

const Login = ({ setUser }) => {
  const [username, setusername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  // 1. Add state to track the loading status
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true); // Set loading to true when the request starts
    setError(''); // Clear any previous errors

    try {
    
      const response = await api.post('/auth/login', {
        username: username,
        password: password,
      });

      const { access_token } = response.data;
      localStorage.setItem('token', access_token); 
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data); 
      navigate('/'); 
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setIsLoading(false); // Set loading to false once the request is finished
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
      <div className="login-header">
          <img src={logo} alt="WealthFy Logo" className="login-logo" />
          <h2>WealthFy</h2>
        </div>
        {error && <p className="error-message">{error}</p>}
        <input
          type="username"
          placeholder="Username"
          value={username}
          onChange={(e) => setusername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {/* 3. Update the button to be disabled and show a message while loading */}
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
        <p className="signup-option">
          Don't have an account? <Link to="/register">Sign Up</Link>
        </p>
      </form>
    </div>
  );
};

export default Login;