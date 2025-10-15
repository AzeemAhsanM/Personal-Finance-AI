import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header/Header.js';
import Navbar from './components/Navbar/Navbar.js';
import Dashboard from './pages/dashboard/dashboard.js';
import Login from './pages/login/login.js';
import Register from './pages/login/register.js';
import './App.css';
import api from './api.js';
import Transactions from './pages/transactions/transactions.js';

function App() {
  const [user, setUser] = useState(null);
  // 1. Add a loading state to wait for the initial user check
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkUser = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // This ensures the token is sent on the initial request
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          const response = await api.get('/auth/me');
          setUser(response.data);
        } catch (error) {
          localStorage.removeItem('token');
        }
      }
      setIsLoading(false); // 2. Stop loading after the check is complete
    };
    checkUser();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  // 3. Show a loading indicator until the initial check is done
  if (isLoading) {
    return <div>Loading Application...</div>;
  }

  return (
    <div className="App">
      {/* 4. Conditionally render the Header and Navbar only if a user is logged in */}
      {user && <Header user={user} onLogout={handleLogout} />}
      {user && <Navbar />}
      <main>
        <Routes>
          {/* If a user is logged in, redirect from /login to the dashboard */}
          <Route path="/login" element={!user ? <Login setUser={setUser} /> : <Navigate to="/dashboard" />} />
          <Route path="/register" element={!user ? <Register /> : <Navigate to="/dashboard" />} />
          
          {/* Protected Routes */}
          <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/transactions" element={user ? <Transactions /> : <Navigate to="/login" />} />
          
          {/* Default Route */}
          <Route path="/" element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;