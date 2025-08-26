import React, { useState } from 'react';
import { toast } from 'react-toastify';

const ExcelImportModal = ({ onImport, onClose }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' && 
          selectedFile.type !== 'application/vnd.ms-excel') {
        toast.error('Lütfen Excel dosyası seçin (.xlsx veya .xls)');
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleImport = async () => {
    if (!file) {
      toast.error('Lütfen bir dosya seçin');
      return;
    }

    setLoading(true);
    
    try {
      // Excel dosyasını okuma işlemi burada yapılacak
      // Şimdilik örnek veri
      const sampleImportedMembers = [
        {
          id: Date.now() + 1,
          photo: '/assets/default-avatar.png',
          name: 'Mehmet Özkan',
          phone: '0534 555 1234',
          email: 'mehmet@example.com',
          graduationYear: 2018,
          university: 'ODTÜ',
          department: 'Makine Mühendisliği',
          status: 'active',
          joinDate: new Date().toISOString(),
          customFields: {}
        },
        {
          id: Date.now() + 2,
          photo: '/assets/default-avatar.png',
          name: 'Ayşe Kaya',
          phone: '0535 555 5678',
          email: 'ayse@example.com',
          graduationYear: 2019,
          university: 'İTÜ',
          department: 'Endüstri Mühendisliği',
          status: 'active',
          joinDate: new Date().toISOString(),
          customFields: {}
        }
      ];
      
      setTimeout(() => {
        onImport(sampleImportedMembers);
        setLoading(false);
      }, 2000);
      
    } catch (error) {
      console.error('Excel import error:', error);
      toast.error('Dosya içe aktarılırken bir hata oluştu');
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">Excel'den Üye İçe Aktarma</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        
        <div className="modal-body">
          <div className="import-instructions">
            <h4>Yönergeler:</h4>
            <ul>
              <li>Excel dosyası şu sütunları içermelidir: Ad Soyad, Telefon, Email, Mezuniyet Yılı, Üniversite, Bölüm</li>
              <li>İlk satır başlık satırı olmalıdır</li>
              <li>Telefon numaraları 05XX XXX XXXX formatında olmalıdır</li>
              <li>Mezuniyet yılı sayısal değer olmalıdır</li>
            </ul>
          </div>
          
          <div className="file-upload">
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileChange}
              className="form-control"
              id="excel-file"
            />
            <label htmlFor="excel-file" className="file-label">
              {file ? file.name : 'Excel dosyası seçin...'}
            </label>
          </div>
          
          {file && (
            <div className="file-info">
              <p><strong>Dosya:</strong> {file.name}</p>
              <p><strong>Boyut:</strong> {(file.size / 1024).toFixed(2)} KB</p>
            </div>
          )}
        </div>
        
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose} disabled={loading}>
            İptal
          </button>
          <button 
            className="btn btn-primary" 
            onClick={handleImport}
            disabled={!file || loading}
          >
            {loading ? 'İçe Aktarılıyor...' : 'İçe Aktar'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExcelImportModal;
