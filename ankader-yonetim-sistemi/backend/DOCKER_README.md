# ANKADER Backend Docker Kurulumu

Bu dosya, ANKADER Dernek Yönetim Sistemi Backend uygulamasının Docker ile nasıl çalıştırılacağını açıklar.

## Gereksinimler

- Docker Desktop (Windows için)
- Git (opsiyonel)

## Docker ile Çalıştırma

### 1. Docker Image Build Etme

```bash
# Backend dizininde çalıştırın
docker build -t ankader-backend .
```

### 2. Container Çalıştırma

```bash
# Tek seferlik çalıştırma
docker run -p 5000:5000 ankader-backend

# Arka planda çalıştırma
docker run -d -p 5000:5000 --name ankader-backend-container ankader-backend
```

### 3. Docker Compose ile Çalıştırma (Önerilen)

```bash
# Container'ları başlat
docker-compose up -d

# Logları görüntüle
docker-compose logs -f

# Container'ları durdur
docker-compose down
```

## Erişim

Backend uygulaması başarıyla çalıştıktan sonra:

- **Ana URL**: http://localhost:5000
- **Test Endpoint**: http://localhost:5000/api/test
- **Sağlık Kontrolü**: http://localhost:5000/api/health

## Faydalı Docker Komutları

```bash
# Çalışan container'ları listele
docker ps

# Tüm container'ları listele
docker ps -a

# Container'a bağlan
docker exec -it ankader-backend-container bash

# Container'ı durdur
docker stop ankader-backend-container

# Container'ı sil
docker rm ankader-backend-container

# Image'ı sil
docker rmi ankader-backend

# Docker loglarını görüntüle
docker logs ankader-backend-container
```

## Troubleshooting

### Port Problemi
Eğer 5000 portu kullanılıyorsa, farklı bir port kullanın:
```bash
docker run -p 8000:5000 ankader-backend
```

### Container Yeniden Başlatma
```bash
docker-compose restart
```

### Container'ı Temizle ve Yeniden Başlat
```bash
docker-compose down
docker-compose up --build -d
```

## Güvenlik Notları

- Container non-root kullanıcı ile çalışır
- Sadece gerekli portlar açılmıştır (5000)
- Health check mekanizması bulunmaktadır
- .dockerignore ile gereksiz dosyalar dışlanmıştır

## Geliştirme

Geliştirme sırasında volume mount kullanarak kod değişikliklerini anlık görebilirsiniz:

```bash
docker run -p 5000:5000 -v "$(pwd):/app" ankader-backend
```

Veya docker-compose-dev.yml dosyası oluşturarak:

```yaml
version: '3.8'
services:
  ankader-backend:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
```
