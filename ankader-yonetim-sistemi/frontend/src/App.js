import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Components
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Members from './pages/Members';
import Events from './pages/Events';
import Budget from './pages/Budget';
import AdminPanel from './pages/AdminPanel';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// CSS
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogin = (userData, token) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  if (!isAuthenticated) {
    return (
      <div className="App">
        <Router>
          <Routes>
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        </Router>
        <ToastContainer position="top-right" autoClose={3000} />
      </div>
    );
  }

  return (
    <div className="App">
      <Router>
        <div className="app-container">
          <Navbar 
            user={user} 
            onLogout={handleLogout}
            onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          />
          <div className="main-content">
            <Sidebar 
              isOpen={sidebarOpen}
              user={user}
            />
            <div className={`content ${sidebarOpen ? 'content-with-sidebar' : 'content-full'}`}>
              <Routes>
                <Route path="/" element={<Dashboard user={user} />} />
                <Route path="/dashboard" element={<Dashboard user={user} />} />
                <Route path="/members" element={<Members user={user} />} />
                <Route path="/events" element={<Events user={user} />} />
                <Route path="/budget" element={<Budget user={user} />} />
                {user?.role === 'ACAR' && (
                  <Route path="/admin" element={<AdminPanel user={user} />} />
                )}
                <Route path="*" element={<Navigate to="/dashboard" />} />
              </Routes>
            </div>
          </div>
        </div>
      </Router>
      <ToastContainer position="top-right" autoClose={3000} />
    </div>
  );
}

export default App;
