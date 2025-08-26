import React from 'react';
import './AdminPanel.css';

const AdminPanel = ({ user }) => {
  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Yönetici Paneli</h1>
        <p>Sistem yönetimi ve kullanıcı ayarları</p>
      </div>
      
      <div className="coming-soon">
        <h2>Çok Yakında!</h2>
        <p>Yönetici paneli modülü geliştirme aşamasındadır.</p>
      </div>
    </div>
  );
};

export default AdminPanel;
