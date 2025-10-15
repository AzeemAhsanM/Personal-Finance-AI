import React, { useState } from 'react';
import { FaUserCircle } from 'react-icons/fa';
import logo from './../../assets/logo.png';
import './Header.css';

function Header({user, onLogout}) {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen)
    };

    return(
        <header className='header-container'>
        <div className='header-brand'>
        <img src = {logo} alt="WealthFy Logo" className='header-logo'/>
        <h1 className='header-title'>WealthFy</h1>
        </div>

        <div className='user-menu'>
            <FaUserCircle className='user-icon' onClick={toggleDropdown}/>
            {isDropdownOpen && (
            <div className='dropdown-menu'>
                <div className='dropdown-items'>{user.username}</div>
                <div className='dropdown-items' onClick={onLogout}>Logout</div>
            </div>
            )}
        </div>
        </header>
    ); 
}
export default Header;