@echo off
echo ========================================
echo   ANKADER Tam Sistem Baslatiyor...
echo ========================================
echo.

echo MongoDB baslatiyor...
start "MongoDB" cmd /k "mongod"
timeout /t 3

echo Backend baslatiyor...
start "ANKADER Backend" cmd /k "cd backend && npm run dev"
timeout /t 3

echo Frontend baslatiyor...
start "ANKADER Frontend" cmd /k "cd frontend && npm start"

echo.
echo Tum servisler baslatildi!
echo.
echo - MongoDB: Arka planda calisiyor
echo - Backend: http://localhost:5000
echo - Frontend: http://localhost:3000
echo.
echo Ana yonetici bilgileri:
echo - Ad: ACAR
echo - Telefon: 05000000000  
echo - Sifre: acar2024!
echo.
pause
