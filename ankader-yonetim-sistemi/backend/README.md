# ANKADER Backend - Python Flask

Bu proje ANKADER Dernek Yönetim Sistemi'nin Python Flask ile yazılmış backend kısmıdır.

## Kurulum

1. Python 3.8+ yüklü olduğundan emin olun
2. Gerekli paketleri kurun:
   ```bash
   pip install -r requirements.txt
   ```

## Çalıştırma

### Yöntem 1: Python ile direkt
```bash
python app.py
```

### Yöntem 2: Batch dosyası ile
```bash
start-python.bat
```

## API Endpoint'leri

- `GET /` - Ana sayfa
- `GET /api/test` - Test endpoint'i
- `POST /api/auth/login` - Kullanıcı girişi
- `POST /api/auth/log-activity` - Aktivite kaydı

## Varsayılan Kullanıcı

- **Ad**: ACAR
- **Telefon**: 05000000000
- **Şifre**: acar2024!

## Port

Sunucu varsayılan olarak `http://localhost:5000` adresinde çalışır.

## Teknolojiler

- Python 3.12+
- Flask 2.3.3
- Flask-CORS 4.0.0

## Notlar

- CORS tüm origin'ler için etkinleştirilmiştir
- Debug modu açıktır (production'da kapatılmalıdır)
- Kullanıcı verileri bellekte tutulur (production'da veritabanı kullanılmalıdır)
