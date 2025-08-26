import React, { useState } from 'react';
import { toast } from 'react-toastify';
import authService from '../services/authService';
import './Login.css';

const Login = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.phone || !formData.password) {
      toast.error('Lütfen tüm alanları doldurun');
      return;
    }

    setLoading(true);
    
    try {
      const response = await authService.login(formData);
      
      if (response.success) {
        toast.success('Giriş başarılı!');
        onLogin(response.user, response.token);
        
        // Giriş logunu kaydet
        await authService.logActivity({
          userId: response.user.id,
          activity: 'Sisteme giriş yaptı',
          timestamp: new Date().toISOString()
        });
      } else {
        toast.error(response.message || 'Giriş başarısız');
      }
    } catch (error) {
      console.error('Login error:', error);
      toast.error('Bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <div className="logo-container">
            <img 
              src="/assets/ankader-logo.png" 
              alt="ANKADER Logo" 
              className="logo"
            />
          </div>
          <h1>ANKADER</h1>
          <p>Yönetim Sistemi</p>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="name" className="form-label">
              Ad Soyad
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="form-control"
              placeholder="Ad soyadınızı girin"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="phone" className="form-label">
              Telefon
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="form-control"
              placeholder="Telefon numaranızı girin"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Şifre
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="form-control"
              placeholder="Şifrenizi girin"
              required
            />
          </div>
          
          <button 
            type="submit" 
            className={`btn btn-primary login-btn ${loading ? 'loading' : ''}`}
            disabled={loading}
          >
            {loading ? (
              <div className="spinner"></div>
            ) : (
              'Giriş Yap'
            )}
          </button>
        </form>
        
        <div className="login-footer">
          <p>Bu sistem sadece yetkili yöneticiler içindir.</p>
          <p className="motto">"Küllerinden Doğuyor"</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
