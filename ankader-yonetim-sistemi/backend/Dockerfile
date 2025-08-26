# Base image olarak Python 3.9'u kullan
FROM python:3.9-slim

# Maintainer bilgisi
LABEL maintainer="ANKADER Yönetim Sistemi"
LABEL description="ANKADER Dernek Yönetim Sistemi Backend API - Python Flask"
LABEL version="1.0.0"

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları çalışma dizinine kopyala
COPY requirements.txt requirements.txt

# Bağımlılıkları yükle (Gunicorn dahil)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Uygulama kodlarını kopyala
COPY . .

# Gunicorn'u çalıştırırken kullanılacak portu belirt
EXPOSE 5000

# Flask uygulamasını Gunicorn ile başlat
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
