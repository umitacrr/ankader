# ANKADER Dernek Yönetim Sistemi

**Pendik İTO Şehit Ahmet Aslanhan Anadolu İmam Hatip Lisesi Mezunları ve Mensupları Derneği** için geliştirilmiş kapsamlı web tabanlı yönetim sistemi.

## 🎯 Proje Hakkında

Bu sistem, ANKADER derneğinin tüm yönetim süreçlerini dijitalleştirmek ve verimli bir şekilde yönetmek için geliştirilmiştir. Sadece yetkili yöneticiler tarafından kullanılmak üzere tasarlanmıştır.

### ✨ Temel Özellikler

- **Üye Yönetimi**: Kapsamlı üye veritabanı, Excel import/export
- **Etkinlik Takibi**: Etkinlik planlama, katılımcı yönetimi, geri bildirim
- **Bütçe Yönetimi**: Gelir-gider takibi, raporlama
- **Yönetici Paneli**: Kullanıcı yönetimi, sistem ayarları, aktivite logları
- **Güvenlik**: Role-based erişim kontrolü, aktivite logları

## 🚀 Teknoloji Stack

### Frontend
- **React.js** 18.x
- **React Router** - Sayfa yönlendirme
- **Material-UI** - UI bileşenleri
- **Chart.js** - Grafik ve istatistikler
- **Axios** - API istekleri
- **React Toastify** - Bildirimler

### Backend
- **Node.js** & **Express.js**
- **MongoDB** & **Mongoose**
- **JWT** - Kimlik doğrulama
- **Bcrypt** - Şifre şifreleme
- **Multer** - Dosya yükleme
- **Express Validator** - Veri doğrulama

## 🏗️ Kurulum

### Ön Gereksinimler
- Node.js (v16 veya üzeri)
- MongoDB (v5 veya üzeri)
- Git

### 1. Projeyi İndirin
```bash
git clone <repository-url>
cd ankader-yonetim-sistemi
```

### 2. Backend Kurulumu
```bash
cd backend
npm install
```

### 3. Frontend Kurulumu
```bash
cd frontend
npm install
```

### 4. Ortam Değişkenlerini Ayarlayın
Backend klasöründe `.env` dosyasını düzenleyin:
```env
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://localhost:27017/ankader
JWT_SECRET=your-very-secure-jwt-secret
FRONTEND_URL=http://localhost:3000
```

### 5. MongoDB'yi Başlatın
```bash
mongod
```

### 6. Uygulamayı Çalıştırın

**Backend:**
```bash
cd backend
npm run dev
```

**Frontend:**
```bash
cd frontend
npm start
```

Uygulama `http://localhost:3000` adresinde çalışacaktır.

## 👤 İlk Giriş

Sistem ilk çalıştırıldığında otomatik olarak ana yönetici hesabı oluşturulur:

- **Ad:** ACAR
- **Telefon:** 05000000000
- **Şifre:** acar2024!

⚠️ **Güvenlik:** İlk girişten sonra şifrenizi mutlaka değiştirin!

## 📋 Kullanım Kılavuzu

### Üye Yönetimi
1. **Tek Tek Üye Ekleme**: Manuel form ile yeni üye kaydı
2. **Excel'den İçe Aktarma**: Toplu üye yükleme
3. **Üye Düzenleme**: Mevcut üye bilgilerini güncelleme
4. **Arama ve Filtreleme**: Mezuniyet yılı, üniversite, durum bazlı filtreleme
5. **Özel Alanlar**: İhtiyaca göre ek bilgi alanları

### Etkinlik Takibi
1. **Etkinlik Oluşturma**: Detaylı etkinlik planlama
2. **Katılımcı Yönetimi**: Kayıt ve katılım takibi
3. **Bütçe Takibi**: Etkinlik masrafları ve gelirleri
4. **Geri Bildirim**: Katılımcı değerlendirmeleri

### Bütçe Yönetimi
1. **Gelir Kaydı**: Çeşitli gelir türlerinin takibi
2. **Gider Kaydı**: Harcama kategorileri ve takibi
3. **Raporlama**: Grafik ve tablolar ile analiz
4. **Bütçe Planlaması**: Dönemsel bütçe yönetimi

### Admin Paneli (Sadece ACAR)
1. **Kullanıcı Yönetimi**: Yönetici hesapları oluşturma/düzenleme
2. **Yetki Yönetimi**: Role-based erişim kontrolü
3. **Aktivite Logları**: Tüm sistem aktivitelerini görüntüleme
4. **Sistem Ayarları**: Genel konfigürasyon

## 🔒 Güvenlik

- **JWT Token** tabanlı kimlik doğrulama
- **Bcrypt** ile şifre hashleme
- **Role-based** erişim kontrolü
- **Aktivite logları** ile izlenebilirlik
- **Input validation** ile veri güvenliği
- **Rate limiting** ile DDoS koruması

## 📱 Responsive Tasarım

Sistem tüm cihazlarda (masaüstü, tablet, mobil) uyumlu çalışacak şekilde tasarlanmıştır.

## 🎨 Tema ve Tasarım

ANKADER'ın kurumsal rengi olan **turuncu (#ff7f00)** teması kullanılmıştır. Temiz, modern ve kullanıcı dostu arayüz tasarımı.

## 📊 Raporlama

- Üye istatistikleri
- Etkinlik katılım analizleri
- Bütçe raporları
- Zaman bazlı trendler
- Excel export özelliği

## 🔧 Özelleştirme

### Özel Alanlar Ekleme
Üye bilgilerine özel alanlar eklemek için:
1. Admin panelinden "Özel Alan Ekle" seçeneği
2. Alan adı ve türünü belirleyin
3. Tüm üyeler için otomatik olarak kullanılabilir hale gelir

### Tema Özelleştirme
`frontend/src/App.css` dosyasından renk şeması değiştirilebilir.

## 🚀 Production Deploy

### Backend Deploy
```bash
cd backend
npm run build
npm start
```

### Frontend Deploy
```bash
cd frontend
npm run build
# Build klasörünü web sunucunuza yükleyin
```

### Ortam Değişkenleri (Production)
```env
NODE_ENV=production
MONGODB_URI=your-production-mongodb-uri
JWT_SECRET=your-production-jwt-secret
FRONTEND_URL=https://your-domain.com
```

## 🔄 Backup ve Restore

### MongoDB Backup
```bash
mongodump --db ankader --out ./backup
```

### MongoDB Restore
```bash
mongorestore --db ankader ./backup/ankader
```

## 📝 Lisans

Bu proje ANKADER derneği için özel olarak geliştirilmiştir.

## 🤝 Destek

Teknik destek için: [iletişim bilgileri]

## 📈 Gelecek Güncellemeler

- [ ] SMS bildirimleri
- [ ] Email entegrasyonu
- [ ] Mobil uygulama
- [ ] Gelişmiş raporlama
- [ ] Otomatik yedekleme
- [ ] API dokumentasyonu

---

**ANKADER - "Küllerinden Doğuyor"**

*Pendik İTO Şehit Ahmet Aslanhan Anadolu İmam Hatip Lisesi Mezunları ve Mensupları Derneği*
