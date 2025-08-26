import React from 'react';
import './Events.css';

const Events = ({ user }) => {
  return (
    <div className="events-page">
      <div className="page-header">
        <h1>Etkinlik Takibi</h1>
        <p>Dernek etkinliklerini yönetin ve takip edin</p>
      </div>
      
      <div className="coming-soon">
        <h2>Çok Yakında!</h2>
        <p>Etkinlik yönetim modülü geliştirme aşamasındadır.</p>
      </div>
    </div>
  );
};

export default Events;
