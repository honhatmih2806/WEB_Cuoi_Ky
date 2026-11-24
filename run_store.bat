@echo off
chcp 65001 >nul
title UteTechStore — Electronics Store Launcher
color 0B

echo ==============================================================================
echo       UteTechStore (UTE TECH STORE) - PREMIUM ELECTRONICS STORE
echo ==============================================================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set DISABLE_SQLALCHEMY_CEXT=1

:: 1. Check Python
if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    set "PY_CMD=%SCRIPT_DIR%.venv\Scripts\python.exe"
    echo [OK] Su dung Python tu Virtual Environment: .venv
) else (
    set "PY_CMD=python"
    echo [INFO] Su dung Python he thong.
)

:: 2. Check Node
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [CANH BAO] Khong tim thay Node.js / npm trong PATH! Vui long cai dat Node.js.
)

echo.
echo [1/2] Khoi dong Backend FastAPI (http://localhost:8000) ...
start "UteTechStore — Backend API (FastAPI)" cmd /k "cd /d "%SCRIPT_DIR%apps\api" && set DISABLE_SQLALCHEMY_CEXT=1 && "%PY_CMD%" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [2/2] Khoi dong Frontend Next.js (http://localhost:3000) ...
start "UteTechStore — Frontend Web (Next.js)" cmd /k "cd /d "%SCRIPT_DIR%apps\web" && npm run dev"

timeout /t 4 /nobreak >nul

echo.
echo ==============================================================================
echo [THANH CONG] Toan bo he thong UteTechStore da duoc khoi chay!
echo.
echo  - Cua hang Truc Tuyen: http://localhost:3000
echo  - Tai lieu API (Swagger): http://localhost:8000/docs
echo  - Kiem tra ket noi:    http://localhost:8000/health
echo ==============================================================================
echo.
echo Dang mo trinh duyet den http://localhost:3000 ...
start http://localhost:3000
exit
