import React from 'react';

const MemberDetailModal = ({ member, onClose, onEdit }) => {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">Üye Detayları</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        
        <div className="modal-body">
          <div className="member-detail-photo">
            <img src={member.photo} alt={member.name} />
          </div>
          
          <div className="member-detail-info">
            <h2>{member.name}</h2>
            <p><strong>Telefon:</strong> {member.phone}</p>
            <p><strong>Email:</strong> {member.email}</p>
            <p><strong>Mezuniyet Yılı:</strong> {member.graduationYear}</p>
            <p><strong>Üniversite:</strong> {member.university}</p>
            <p><strong>Bölüm:</strong> {member.department}</p>
            <p><strong>Durum:</strong> 
              <span className={`status-badge ${member.status}`}>
                {member.status === 'active' ? 'Aktif' : 'Pasif'}
              </span>
            </p>
            <p><strong>Kayıt Tarihi:</strong> {new Date(member.joinDate).toLocaleDateString('tr-TR')}</p>
            
            {member.customFields && Object.keys(member.customFields).length > 0 && (
              <div className="custom-fields">
                <h4>Ek Bilgiler</h4>
                {Object.entries(member.customFields).map(([key, value]) => (
                  <p key={key}><strong>{key}:</strong> {value}</p>
                ))}
              </div>
            )}
            
            {member.notes && (
              <div className="member-notes">
                <h4>Notlar</h4>
                <p>{member.notes}</p>
              </div>
            )}
          </div>
        </div>
        
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Kapat</button>
          <button className="btn btn-primary" onClick={onEdit}>Düzenle</button>
        </div>
      </div>
    </div>
  );
};

export default MemberDetailModal;
