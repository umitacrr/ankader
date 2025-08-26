import React from 'react';
import './Budget.css';

const Budget = ({ user }) => {
  return (
    <div className="budget-page">
      <div className="page-header">
        <h1>Bütçe Yönetimi</h1>
        <p>Dernek gelir ve giderlerini takip edin</p>
      </div>
      
      <div className="coming-soon">
        <h2>Çok Yakında!</h2>
        <p>Bütçe yönetim modülü geliştirme aşamasındadır.</p>
      </div>
    </div>
  );
};

export default Budget;
