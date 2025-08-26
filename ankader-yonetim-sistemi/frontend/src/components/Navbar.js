import React from 'react';
import { FaBars, FaSignOutAlt, FaUser } from 'react-icons/fa';
import './Navbar.css';

const Navbar = ({ user, onLogout, onToggleSidebar }) => {
  const handleLogout = () => {
    if (window.confirm('Çıkış yapmak istediğinizden emin misiniz?')) {
      onLogout();
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button 
          className="sidebar-toggle"
          onClick={onToggleSidebar}
          aria-label="Toggle Sidebar"
        >
          <FaBars />
        </button>
        
        <div className="navbar-brand">
          <img 
            src="/assets/ankader-logo.png" 
            alt="ANKADER" 
            className="navbar-logo"
          />
          <span className="brand-text">ANKADER Yönetim</span>
        </div>
      </div>
      
      <div className="navbar-right">
        <div className="user-info">
          <FaUser className="user-icon" />
          <span className="user-name">{user?.name}</span>
          {user?.role === 'ACAR' && (
            <span className="user-role">Ana Yönetici</span>
          )}
        </div>
        
        <button 
          className="logout-btn"
          onClick={handleLogout}
          title="Çıkış Yap"
        >
          <FaSignOutAlt />
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
