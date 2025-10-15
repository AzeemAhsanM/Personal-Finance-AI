import React from 'react';
// 1. Import NavLink from react-router-dom
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar-container">
      <NavLink to="/dashboard" className="nav-link">Dashboard</NavLink>
      <NavLink to="/transactions" className="nav-link">Transactions</NavLink>
      <NavLink to="/add" className="nav-link">Add New</NavLink>
      <NavLink to="/finbot" className="nav-link">FinBot AI</NavLink>
      <NavLink to="/calculator" className="nav-link">Calculator</NavLink>
    </nav>
  );
}

export default Navbar;