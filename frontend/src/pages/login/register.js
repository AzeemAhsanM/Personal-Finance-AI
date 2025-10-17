import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../api'; 
import logo from '../../assets/logo.png';
import './login.css'; 

function Register() {
  // 1. State for all necessary fields
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');

    // 2. Client-side validation for matching passwords
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return; // Stop the function if passwords don't match
    }

    setIsLoading(true);

    try {
      // 3. API call to the /auth/register endpoint
      await api.post('/auth/register', {
        username: username,
        password: password,
      });

      // 4. Redirect to the login page on success
      navigate('/'); 
    } catch (err) {
      // Handle errors from the backend (e.g., user already exists)
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleRegister} className="login-form">
        <div className="login-header">
          <img src={logo} alt="WealthFy Logo" className="login-logo" />
          <h2>Create Your Account</h2>
        </div>

        {error && <p className="error-message">{error}</p>}

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Registering...' : 'Register'}
        </button>

        <p className="signup-option">
          Already have an account? <Link to="/">Login</Link>
        </p>
      </form>
    </div>
  );
}

export default Register;