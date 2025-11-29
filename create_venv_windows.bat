@echo off
echo ==============================================
echo   Create Python Virtual Environment (.venv)
echo   Windows CMD / PowerShell
echo ==============================================
echo.

REM Check Python availability
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python tidak ditemukan!
    echo Install Python terlebih dahulu dari https://python.org
    pause
    exit /b
)

echo 🔧 Membuat virtual environment .venv ...
python -m venv .venv

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Gagal membuat virtual environment.
    pause
    exit /b
)

echo.
echo ✅ Virtual environment .venv berhasil dibuat!
echo.

echo Cara mengaktifkan venv:
echo ----------------------------------------------
echo Windows CMD:
echo     .venv\Scripts\activate
echo.
echo Windows PowerShell:
echo     .venv\Scripts\Activate.ps1
echo ----------------------------------------------
echo.

echo Selesai!
pause

