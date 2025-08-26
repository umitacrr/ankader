import React, { useState, useEffect } from 'react';
import { 
  FaUsers, 
  FaCalendarAlt, 
  FaMoneyBillWave, 
  FaChartLine,
  FaUserPlus,
  FaCalendarPlus
} from 'react-icons/fa';
import { Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import './Dashboard.css';

// Chart.js kayıt
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard = ({ user }) => {
  const [stats, setStats] = useState({
    totalMembers: 0,
    activeMembers: 0,
    totalEvents: 0,
    upcomingEvents: 0,
    totalBudget: 0,
    totalExpenses: 0
  });
  
  const [recentActivities, setRecentActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      // API çağrıları burada yapılacak
      // Şimdilik örnek veri
      setStats({
        totalMembers: 156,
        activeMembers: 142,
        totalEvents: 24,
        upcomingEvents: 3,
        totalBudget: 45000,
        totalExpenses: 32500
      });
      
      setRecentActivities([
        {
          id: 1,
          activity: 'Yeni üye eklendi: Ahmet Yılmaz',
          timestamp: '10 dakika önce',
          type: 'member'
        },
        {
          id: 2,
          activity: 'Etkinlik düzenlendi: Mezunlar Buluşması',
          timestamp: '2 saat önce',
          type: 'event'
        },
        {
          id: 3,
          activity: 'Bütçe güncellendi',
          timestamp: '5 saat önce',
          type: 'budget'
        }
      ]);
    } catch (error) {
      console.error('Dashboard verileri yüklenirken hata:', error);
    } finally {
      setLoading(false);
    }
  };

  // Grafik verileri
  const memberStatsData = {
    labels: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran'],
    datasets: [
      {
        label: 'Yeni Üyeler',
        data: [12, 19, 15, 25, 22, 18],
        borderColor: '#ff7f00',
        backgroundColor: 'rgba(255, 127, 0, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const budgetData = {
    labels: ['Gelir', 'Gider', 'Kalan'],
    datasets: [
      {
        data: [45000, 32500, 12500],
        backgroundColor: ['#28a745', '#dc3545', '#ff7f00'],
        borderWidth: 0,
      },
    ],
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Hoş Geldiniz, {user?.name}</h1>
        <p>ANKADER Yönetim Sistemi Dashboard</p>
      </div>

      {/* İstatistik Kartları */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon members">
            <FaUsers />
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.totalMembers}</div>
            <div className="stat-label">Toplam Üye</div>
            <div className="stat-subtitle">{stats.activeMembers} aktif</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon events">
            <FaCalendarAlt />
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.totalEvents}</div>
            <div className="stat-label">Toplam Etkinlik</div>
            <div className="stat-subtitle">{stats.upcomingEvents} yaklaşan</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon budget">
            <FaMoneyBillWave />
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.totalBudget.toLocaleString('tr-TR')} ₺</div>
            <div className="stat-label">Toplam Bütçe</div>
            <div className="stat-subtitle">{stats.totalExpenses.toLocaleString('tr-TR')} ₺ harcandı</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon growth">
            <FaChartLine />
          </div>
          <div className="stat-info">
            <div className="stat-value">%15</div>
            <div className="stat-label">Büyüme Oranı</div>
            <div className="stat-subtitle">Bu ay</div>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        {/* Sol Kolon - Grafikler */}
        <div className="dashboard-left">
          <div className="card">
            <div className="card-header">
              <h3>Üye İstatistikleri</h3>
            </div>
            <div className="card-body">
              <Line 
                data={memberStatsData} 
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'top',
                    },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                }}
              />
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h3>Bütçe Dağılımı</h3>
            </div>
            <div className="card-body">
              <div className="chart-container">
                <Doughnut 
                  data={budgetData}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                    },
                  }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Sağ Kolon - Son Aktiviteler ve Hızlı İşlemler */}
        <div className="dashboard-right">
          <div className="card">
            <div className="card-header">
              <h3>Hızlı İşlemler</h3>
            </div>
            <div className="card-body">
              <div className="quick-actions">
                <button className="quick-action-btn members">
                  <FaUserPlus />
                  <span>Yeni Üye Ekle</span>
                </button>
                <button className="quick-action-btn events">
                  <FaCalendarPlus />
                  <span>Etkinlik Oluştur</span>
                </button>
                <button className="quick-action-btn budget">
                  <FaMoneyBillWave />
                  <span>Harcama Ekle</span>
                </button>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h3>Son Aktiviteler</h3>
            </div>
            <div className="card-body">
              <div className="activities-list">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className={`activity-item ${activity.type}`}>
                    <div className="activity-content">
                      <p className="activity-text">{activity.activity}</p>
                      <span className="activity-time">{activity.timestamp}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Yaklaşan Etkinlikler */}
          <div className="card">
            <div className="card-header">
              <h3>Yaklaşan Etkinlikler</h3>
            </div>
            <div className="card-body">
              <div className="upcoming-events">
                <div className="event-item">
                  <div className="event-date">
                    <span className="day">15</span>
                    <span className="month">Ağu</span>
                  </div>
                  <div className="event-info">
                    <h4>Mezunlar Buluşması</h4>
                    <p>Saat: 19:00 - Lokasyon: Okul Bahçesi</p>
                  </div>
                </div>
                <div className="event-item">
                  <div className="event-date">
                    <span className="day">22</span>
                    <span className="month">Ağu</span>
                  </div>
                  <div className="event-info">
                    <h4>Yönetim Kurulu Toplantısı</h4>
                    <p>Saat: 20:00 - Lokasyon: Online</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
