@echo off
chcp 65001 >nul
echo ========================================
echo Log Cleaner - EXE Oluşturucu
echo ========================================
echo.

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadı!
    echo Lütfen Python'u kurun: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] PyInstaller kuruluyor...
python -m pip install --upgrade pip
python -m pip install pyinstaller

if errorlevel 1 (
    echo [HATA] PyInstaller kurulumu başarısız!
    pause
    exit /b 1
)

echo.
echo [2/3] EXE dosyasi olusturuluyor...
echo Bu işlem birkaç dakika sürebilir...
echo.

python -m PyInstaller --onefile ^
    --console ^
    --name "LogCleaner" ^
    --add-data "README.md;." ^
    --hidden-import=pathlib ^
    --hidden-import=shutil ^
    --clean ^
    log_cleaner.py

if errorlevel 1 (
    echo [HATA] EXE oluşturma başarısız!
    pause
    exit /b 1
)

echo.
echo [3/3] Temizlik yapılıyor...
if exist build rmdir /s /q build
if exist LogCleaner.spec del LogCleaner.spec

echo.
echo ========================================
echo ✅ TAMAMLANDI!
echo ========================================
echo.
echo EXE dosyasi: dist\LogCleaner.exe
echo.
echo Dosyayi çalıştırmak için:
echo   dist\LogCleaner.exe
echo.
pause
