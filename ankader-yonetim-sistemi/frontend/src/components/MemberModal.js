import React, { useState } from 'react';

const MemberModal = ({ member, editMode, onSave, onClose }) => {
  const [formData, setFormData] = useState({
    name: member?.name || '',
    phone: member?.phone || '',
    email: member?.email || '',
    graduationYear: member?.graduationYear || new Date().getFullYear(),
    university: member?.university || '',
    department: member?.department || '',
    status: member?.status || 'active',
    notes: member?.notes || ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">
            {editMode ? 'Üye Düzenle' : 'Yeni Üye Ekle'}
          </h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label className="form-label">Ad Soyad *</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Telefon *</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Email *</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Mezuniyet Yılı *</label>
              <input
                type="number"
                name="graduationYear"
                value={formData.graduationYear}
                onChange={handleChange}
                className="form-control"
                min="1990"
                max={new Date().getFullYear()}
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Üniversite *</label>
              <input
                type="text"
                name="university"
                value={formData.university}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Bölüm *</label>
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Durum</label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="form-control"
              >
                <option value="active">Aktif</option>
                <option value="inactive">Pasif</option>
              </select>
            </div>
            
            <div className="form-group">
              <label className="form-label">Notlar</label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                className="form-control"
                rows="3"
              />
            </div>
          </div>
          
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              İptal
            </button>
            <button type="submit" className="btn btn-primary">
              {editMode ? 'Güncelle' : 'Kaydet'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MemberModal;
