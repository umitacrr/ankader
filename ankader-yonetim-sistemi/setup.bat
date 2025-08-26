@echo off
echo ========================================
echo   ANKADER Yonetim Sistemi Kurulum
echo ========================================
echo.

echo [1/4] Backend bagimliliklari yukleniyor...
cd backend
call npm install
if %errorlevel% neq 0 (
    echo HATA: Backend bagimliliklari yuklenemedi!
    pause
    exit /b 1
)
echo Backend bagimliliklari basariyla yuklendi.
echo.

echo [2/4] Frontend bagimliliklari yukleniyor...
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo HATA: Frontend bagimliliklari yuklenemedi!
    pause
    exit /b 1
)
echo Frontend bagimliliklari basariyla yuklendi.
echo.

echo [3/4] MongoDB baglantisi kontrol ediliyor...
echo MongoDB'nin calistigini kontrol edin: mongod
echo.

echo [4/4] Kurulum tamamlandi!
echo.
echo ========================================
echo   Uygulamayi Calistirmak Icin:
echo ========================================
echo.
echo 1. MongoDB'yi baslatin: mongod
echo 2. Backend'i baslatmak icin: start-backend.bat
echo 3. Frontend'i baslatmak icin: start-frontend.bat
echo.
echo Ana yonetici bilgileri:
echo - Ad: ACAR
echo - Telefon: 05000000000
echo - Sifre: acar2024!
echo.
echo UYARI: Ilk girisden sonra sifrenizi degistirin!
echo.
pause
