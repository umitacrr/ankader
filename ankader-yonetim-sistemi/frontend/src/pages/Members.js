import React, { useState, useEffect } from 'react';
import { 
  FaPlus, 
  FaEdit, 
  FaTrash, 
  FaSearch, 
  FaFileExcel, 
  FaDownload,
  FaEye,
  FaFilter
} from 'react-icons/fa';
import { toast } from 'react-toastify';
import MemberModal from '../components/MemberModal';
import MemberDetailModal from '../components/MemberDetailModal';
import ExcelImportModal from '../components/ExcelImportModal';
import './Members.css';

const Members = ({ user }) => {
  const [members, setMembers] = useState([]);
  const [filteredMembers, setFilteredMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMember, setSelectedMember] = useState(null);
  const [showMemberModal, setShowMemberModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [showExcelModal, setShowExcelModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [filterOptions, setFilterOptions] = useState({
    graduationYear: '',
    university: '',
    status: 'all'
  });

  useEffect(() => {
    fetchMembers();
  }, []);

  useEffect(() => {
    filterMembers();
  }, [searchTerm, members, filterOptions]);

  const fetchMembers = async () => {
    try {
      setLoading(true);
      // API çağrısı burada yapılacak
      // Şimdilik örnek veri
      const sampleMembers = [
        {
          id: 1,
          photo: '/assets/default-avatar.png',
          name: 'Ahmet Yılmaz',
          phone: '0532 123 4567',
          email: 'ahmet@example.com',
          graduationYear: 2020,
          university: 'İstanbul Üniversitesi',
          department: 'Bilgisayar Mühendisliği',
          status: 'active',
          joinDate: '2021-01-15',
          customFields: {
            meslek: 'Yazılım Geliştirici',
            şehir: 'İstanbul'
          }
        },
        {
          id: 2,
          photo: '/assets/default-avatar.png',
          name: 'Fatma Demir',
          phone: '0533 987 6543',
          email: 'fatma@example.com',
          graduationYear: 2019,
          university: 'Boğaziçi Üniversitesi',
          department: 'İktisat',
          status: 'active',
          joinDate: '2020-09-10',
          customFields: {
            meslek: 'Ekonomist',
            şehir: 'Ankara'
          }
        }
      ];
      setMembers(sampleMembers);
    } catch (error) {
      console.error('Üyeler yüklenirken hata:', error);
      toast.error('Üyeler yüklenirken bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const filterMembers = () => {
    let filtered = members.filter(member => {
      const searchMatch = member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         member.phone.includes(searchTerm) ||
                         member.email.toLowerCase().includes(searchTerm.toLowerCase());
      
      const yearMatch = !filterOptions.graduationYear || 
                       member.graduationYear.toString() === filterOptions.graduationYear;
      
      const universityMatch = !filterOptions.university || 
                             member.university.toLowerCase().includes(filterOptions.university.toLowerCase());
      
      const statusMatch = filterOptions.status === 'all' || member.status === filterOptions.status;
      
      return searchMatch && yearMatch && universityMatch && statusMatch;
    });
    
    setFilteredMembers(filtered);
  };

  const handleAddMember = () => {
    setSelectedMember(null);
    setEditMode(false);
    setShowMemberModal(true);
  };

  const handleEditMember = (member) => {
    setSelectedMember(member);
    setEditMode(true);
    setShowMemberModal(true);
  };

  const handleViewMember = (member) => {
    setSelectedMember(member);
    setShowDetailModal(true);
  };

  const handleDeleteMember = async (memberId) => {
    if (window.confirm('Bu üyeyi silmek istediğinizden emin misiniz?')) {
      try {
        // API çağrısı burada yapılacak
        setMembers(members.filter(m => m.id !== memberId));
        toast.success('Üye başarıyla silindi');
      } catch (error) {
        console.error('Üye silinirken hata:', error);
        toast.error('Üye silinirken bir hata oluştu');
      }
    }
  };

  const handleSaveMember = async (memberData) => {
    try {
      if (editMode) {
        // Güncelleme
        setMembers(members.map(m => 
          m.id === selectedMember.id ? { ...memberData, id: selectedMember.id } : m
        ));
        toast.success('Üye bilgileri güncellendi');
      } else {
        // Yeni ekleme
        const newMember = { ...memberData, id: Date.now() };
        setMembers([...members, newMember]);
        toast.success('Yeni üye eklendi');
      }
      setShowMemberModal(false);
    } catch (error) {
      console.error('Üye kaydedilirken hata:', error);
      toast.error('Üye kaydedilirken bir hata oluştu');
    }
  };

  const handleExcelImport = (importedMembers) => {
    setMembers([...members, ...importedMembers]);
    toast.success(`${importedMembers.length} üye başarıyla içe aktarıldı`);
    setShowExcelModal(false);
  };

  const exportToExcel = () => {
    // Excel export işlemi burada yapılacak
    toast.info('Excel dosyası indiriliyor...');
  };

  const getGraduationYears = () => {
    const years = [...new Set(members.map(m => m.graduationYear))].sort((a, b) => b - a);
    return years;
  };

  const getUniversities = () => {
    const universities = [...new Set(members.map(m => m.university))].sort();
    return universities;
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="members-page">
      <div className="page-header">
        <div className="header-left">
          <h1>Üye Yönetimi</h1>
          <p>Toplam {members.length} üye • {filteredMembers.length} gösteriliyor</p>
        </div>
        <div className="header-actions">
          <button className="btn btn-secondary" onClick={exportToExcel}>
            <FaDownload /> Excel İndir
          </button>
          <button className="btn btn-warning" onClick={() => setShowExcelModal(true)}>
            <FaFileExcel /> Excel'den İçe Aktar
          </button>
          <button className="btn btn-primary" onClick={handleAddMember}>
            <FaPlus /> Yeni Üye
          </button>
        </div>
      </div>

      {/* Arama ve Filtre */}
      <div className="filters-section">
        <div className="search-box">
          <FaSearch className="search-icon" />
          <input
            type="text"
            placeholder="Üye ara (ad, telefon, email)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="filter-controls">
          <select
            value={filterOptions.graduationYear}
            onChange={(e) => setFilterOptions({...filterOptions, graduationYear: e.target.value})}
            className="filter-select"
          >
            <option value="">Tüm Mezuniyet Yılları</option>
            {getGraduationYears().map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
          
          <select
            value={filterOptions.university}
            onChange={(e) => setFilterOptions({...filterOptions, university: e.target.value})}
            className="filter-select"
          >
            <option value="">Tüm Üniversiteler</option>
            {getUniversities().map(uni => (
              <option key={uni} value={uni}>{uni}</option>
            ))}
          </select>
          
          <select
            value={filterOptions.status}
            onChange={(e) => setFilterOptions({...filterOptions, status: e.target.value})}
            className="filter-select"
          >
            <option value="all">Tüm Durumlar</option>
            <option value="active">Aktif</option>
            <option value="inactive">Pasif</option>
          </select>
        </div>
      </div>

      {/* Üye Listesi */}
      <div className="members-content">
        {filteredMembers.length === 0 ? (
          <div className="no-members">
            <p>Hiç üye bulunamadı.</p>
          </div>
        ) : (
          <div className="members-grid">
            {filteredMembers.map(member => (
              <div key={member.id} className="member-card">
                <div className="member-photo">
                  <img src={member.photo} alt={member.name} />
                  <div className={`status-badge ${member.status}`}>
                    {member.status === 'active' ? 'Aktif' : 'Pasif'}
                  </div>
                </div>
                
                <div className="member-info">
                  <h3>{member.name}</h3>
                  <p className="member-contact">
                    <span>{member.phone}</span>
                    <span>{member.email}</span>
                  </p>
                  <p className="member-education">
                    {member.university} • {member.graduationYear}
                  </p>
                  <p className="member-department">{member.department}</p>
                </div>
                
                <div className="member-actions">
                  <button
                    className="action-btn view"
                    onClick={() => handleViewMember(member)}
                    title="Detayları Görüntüle"
                  >
                    <FaEye />
                  </button>
                  <button
                    className="action-btn edit"
                    onClick={() => handleEditMember(member)}
                    title="Düzenle"
                  >
                    <FaEdit />
                  </button>
                  <button
                    className="action-btn delete"
                    onClick={() => handleDeleteMember(member.id)}
                    title="Sil"
                  >
                    <FaTrash />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modaller */}
      {showMemberModal && (
        <MemberModal
          member={selectedMember}
          editMode={editMode}
          onSave={handleSaveMember}
          onClose={() => setShowMemberModal(false)}
        />
      )}

      {showDetailModal && selectedMember && (
        <MemberDetailModal
          member={selectedMember}
          onClose={() => setShowDetailModal(false)}
          onEdit={() => {
            setShowDetailModal(false);
            handleEditMember(selectedMember);
          }}
        />
      )}

      {showExcelModal && (
        <ExcelImportModal
          onImport={handleExcelImport}
          onClose={() => setShowExcelModal(false)}
        />
      )}
    </div>
  );
};

export default Members;
