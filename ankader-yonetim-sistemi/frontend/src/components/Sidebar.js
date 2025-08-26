import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  FaTachometerAlt, 
  FaUsers, 
  FaCalendarAlt, 
  FaMoneyBillWave, 
  FaCog,
  FaUserShield 
} from 'react-icons/fa';
import './Sidebar.css';

const Sidebar = ({ isOpen, user }) => {
  const location = useLocation();

  const menuItems = [
    {
      path: '/dashboard',
      icon: FaTachometerAlt,
      label: 'Ana Sayfa',
      role: 'all'
    },
    {
      path: '/members',
      icon: FaUsers,
      label: 'Üye Yönetimi',
      role: 'all'
    },
    {
      path: '/events',
      icon: FaCalendarAlt,
      label: 'Etkinlik Takibi',
      role: 'all'
    },
    {
      path: '/budget',
      icon: FaMoneyBillWave,
      label: 'Bütçe Yönetimi',
      role: 'all'
    },
    {
      path: '/admin',
      icon: FaUserShield,
      label: 'Yönetici Paneli',
      role: 'ACAR'
    }
  ];

  const filteredMenuItems = menuItems.filter(item => 
    item.role === 'all' || user?.role === item.role
  );

  return (
    <aside className={`sidebar ${isOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      <div className="sidebar-content">
        <div className="sidebar-header">
          <h3>Menü</h3>
        </div>
        
        <nav className="sidebar-nav">
          <ul className="nav-list">
            {filteredMenuItems.map((item) => {
              const IconComponent = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <li key={item.path} className="nav-item">
                  <Link
                    to={item.path}
                    className={`nav-link ${isActive ? 'active' : ''}`}
                  >
                    <IconComponent className="nav-icon" />
                    <span className="nav-text">{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
        
        <div className="sidebar-footer">
          <div className="organization-info">
            <h4>ANKADER</h4>
            <p>Pendik İTO Şehit Ahmet Aslanhan Anadolu İmam Hatip Lisesi</p>
            <p className="motto">"Küllerinden Doğuyor"</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
